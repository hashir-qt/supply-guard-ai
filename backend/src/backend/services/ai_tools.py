"""
AI Agent Tools - Functions the AI can call to analyze supply chain data
"""
from typing import List, Dict
from sqlmodel import Session, select
from backend.models.schemas import Supplier, Outlet, Risk, RiskSeverity
from backend.data.enrichment import enrich_supplier, enrich_suppliers, enrich_outlets
from backend.services.cascade_simulator import CascadeSimulator

class SupplyChainTools:
    """Tools that the AI agent can use to answer questions"""
    
    def __init__(self, session: Session):
        self.session = session
        self.simulator = CascadeSimulator()
    
    def get_top_risks(self, limit: int = 5) -> List[Dict]:
        """Get the top N highest priority risks"""
        risks = self.session.exec(select(Risk).where(Risk.status == "active")).all()
        sorted_risks = sorted(risks, key=lambda r: r.risk_score, reverse=True)[:limit]
        
        return [
            {
                "risk_id": r.risk_id,
                "title": r.title,
                "severity": r.severity,
                "risk_score": r.risk_score,
                "category": r.category,
                "affected_outlets": len(r.impact.get("outlets", [])) if r.impact else 0,
                "revenue_at_risk_pkr": r.impact.get("revenue_at_risk_pkr", 0) if r.impact else 0
            }
            for r in sorted_risks
        ]
    
    def analyze_supplier(self, supplier_id: str) -> Dict:
        """Get detailed analysis of a specific supplier"""
        supplier = self.session.get(Supplier, supplier_id)
        if not supplier:
            return {"error": f"Supplier {supplier_id} not found"}
        
        enriched = enrich_supplier(supplier)
        
        return {
            "supplier_id": supplier_id,
            "name": supplier.name,
            "risk_score": enriched["risk_score"],
            "status": enriched["current_status"],
            "metrics": supplier.metrics,
            "risk_factors": supplier.risk_factors,
            "active_alerts": supplier.active_alerts or [],
            "location": supplier.location
        }
    
    def get_outlets_at_risk(self, threshold: int = 50) -> List[Dict]:
        """Get outlets with high risk scores"""
        outlets = self.session.exec(select(Outlet)).all()
        enriched = enrich_outlets(outlets)
        
        at_risk = [o for o in enriched if o["current_risk_score"] >= threshold]
        
        return [
            {
                "outlet_id": o["outlet_id"],
                "name": o["name"],
                "city": o["city"],
                "risk_score": o["current_risk_score"],
                "chicken_days": o["inventory"].get("chicken_days_remaining") if o["inventory"] else None
            }
            for o in sorted(at_risk, key=lambda x: x["current_risk_score"], reverse=True)
        ]
    
    def simulate_disruption(self, disruption_type: str, severity: str, duration_days: int) -> Dict:
        """Run a what-if simulation"""
        result = self.simulator.simulate_disruption(disruption_type, severity, duration_days)
        
        timeline = result.get("timeline", [])
        max_outlets = max([stage.get("outlets_affected", 0) for stage in timeline], default=0)
        revenue_loss = self.simulator.estimate_revenue_impact(max_outlets, duration_days)
        
        return {
            "disruption_type": disruption_type,
            "severity": severity,
            "duration_days": duration_days,
            "timeline": timeline,
            "total_outlets_affected": max_outlets,
            "revenue_loss_pkr": revenue_loss,
            "revenue_loss_formatted": f"PKR {revenue_loss/10000000:.1f} Cr"
        }
    
    def get_supplier_alternatives(self, supplier_id: str) -> List[Dict]:
        """Find alternative suppliers"""
        current = self.session.get(Supplier, supplier_id)
        if not current:
            return []
        
        all_suppliers = self.session.exec(select(Supplier)).all()
        enriched = enrich_suppliers([s for s in all_suppliers if s.supplier_id != supplier_id and s.type == current.type])
        
        return [
            {
                "supplier_id": s["supplier_id"],
                "name": s["name"],
                "risk_score": s["risk_score"],
                "reliability": s["metrics"].get("reliability", 0) if s["metrics"] else 0,
                "city": s["location"].get("city") if s["location"] else "Unknown"
            }
            for s in sorted(enriched, key=lambda x: x["risk_score"])[:3]
        ]
    
    def get_low_inventory_outlets(self, threshold: float = 2.0) -> List[Dict]:
        """Get outlets with critically low inventory"""
        outlets = self.session.exec(select(Outlet)).all()
        
        low_stock = [
            o for o in outlets 
            if o.inventory and o.inventory.get("chicken_days_remaining", 99) < threshold
        ]
        
        return [
            {
                "outlet_id": o.outlet_id,
                "name": o.name,
                "city": o.city,
                "chicken_days": o.inventory.get("chicken_days_remaining"),
                "status": "critical" if o.inventory.get("chicken_days_remaining", 0) < 1.5 else "warning"
            }
            for o in sorted(low_stock, key=lambda x: x.inventory.get("chicken_days_remaining", 0))
        ]

# Tool definitions for OpenAI function calling
TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "get_top_risks",
            "description": "Get the highest priority supply chain risks currently active",
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Number of risks to return", "default": 5}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_supplier",
            "description": "Get detailed analysis of a specific supplier including risk score and metrics",
            "parameters": {
                "type": "object",
                "properties": {
                    "supplier_id": {"type": "string", "description": "Supplier ID (e.g., SUP-001)"}
                },
                "required": ["supplier_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_outlets_at_risk",
            "description": "Get outlets with high risk scores",
            "parameters": {
                "type": "object",
                "properties": {
                    "threshold": {"type": "integer", "description": "Minimum risk score threshold", "default": 50}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "simulate_disruption",
            "description": "Run a what-if simulation to model supply chain disruption scenarios",
            "parameters": {
                "type": "object",
                "properties": {
                    "disruption_type": {"type": "string", "description": "Type: supplier_failure, logistics_delay, demand_surge"},
                    "severity": {"type": "string", "description": "Severity: low, medium, high, critical"},
                    "duration_days": {"type": "integer", "description": "Duration in days"}
                },
                "required": ["disruption_type", "severity", "duration_days"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_supplier_alternatives",
            "description": "Find alternative suppliers of the same type",
            "parameters": {
                "type": "object",
                "properties": {
                    "supplier_id": {"type": "string", "description": "Current supplier ID"}
                },
                "required": ["supplier_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_low_inventory_outlets",
            "description": "Get outlets with critically low chicken inventory",
            "parameters": {
                "type": "object",
                "properties": {
                    "threshold": {"type": "number", "description": "Days of inventory threshold", "default": 2.0}
                }
            }
        }
    }
]
