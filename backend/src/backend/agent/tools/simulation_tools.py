"""Simulation Tools - Using OpenAI Agents SDK"""
from agents import function_tool
from sqlmodel import select

from backend.database import get_session
from backend.models.schemas import Supplier, Outlet
from backend.data.enrichment import enrich_suppliers
from backend.services.cascade_simulator import CascadeSimulator

@function_tool
def simulate_disruption(
    disruption_type: str,
    entity_id: str,
    severity: str = "high",
    duration_days: int = 7
) -> dict:
    """
    Simulate cascading impact of a supply chain disruption.
    
    Args:
        disruption_type: "supplier_failure", "route_blocked", "demand_surge"
        entity_id: ID of affected entity (e.g. "SUP-001" for K&N's)
        severity: "low", "medium", "high", "critical"
        duration_days: how long the disruption lasts
    
    Returns:
    - Cascade timeline day-by-day
    - Total outlets affected
    - Revenue loss in PKR
    - Prevention recommendations
    
    Use when user asks:
    - "What if K&N's shuts down?"
    - "Simulate monsoon flooding"
    - "What happens if we lose supplier X?"
    """
    with next(get_session()) as session:
        simulator = CascadeSimulator()
        
        # Get entity info
        entity_name = entity_id
        if disruption_type == "supplier_failure":
            supplier = session.get(Supplier, entity_id)
            if supplier:
                entity_name = supplier.name
        
        # Run simulation
        result = simulator.simulate_disruption(disruption_type, severity, duration_days)
        timeline = result.get("timeline", [])
        
        # Calculate impact
        peak_outlets = max([s.get("outlets_affected", 0) for s in timeline], default=5)
        revenue_per_outlet = 500000  # PKR 5 Lakh/day
        revenue_loss = peak_outlets * revenue_per_outlet * duration_days
        customers_lost = peak_outlets * 350 * duration_days
        
        cascade = []
        for i, stage in enumerate(timeline):
            cascade.append({
                "day": i * 2,
                "outlets_affected": stage.get("outlets_affected", i * 2),
                "status": stage.get("description", "Impact spreading")
            })
        
        return {
            "scenario": {
                "disruption": disruption_type,
                "entity": entity_name,
                "severity": severity,
                "duration_days": duration_days
            },
            "cascade_timeline": cascade,
            "total_impact": {
                "peak_outlets": peak_outlets,
                "revenue_loss_pkr": revenue_loss,
                "revenue_formatted": f"PKR {revenue_loss/10000000:.1f} Cr",
                "customers_lost": customers_lost
            },
            "prevention": [
                f"Contact backup suppliers for {entity_name} NOW",
                "Implement limited menu at risk outlets",
                "Pre-position emergency inventory",
                "Prepare customer communication"
            ]
        }

@function_tool
def get_simulation_scenarios() -> dict:
    """
    Get predefined simulation scenarios based on current risks.
    
    Use when user asks:
    - "What scenarios can we simulate?"
    - "Show me simulation options"
    """
    with next(get_session()) as session:
        suppliers = session.exec(select(Supplier)).all()
        enriched = enrich_suppliers(suppliers)
        at_risk = [s for s in enriched if s["risk_score"] >= 60]
        
        scenarios = [
            {"id": "kns_failure", "name": "K&N's Shutdown", "entity_id": "SUP-001", "type": "supplier_failure"},
            {"id": "monsoon", "name": "Karachi Monsoon", "entity_id": "karachi", "type": "route_blocked"},
            {"id": "psl_surge", "name": "PSL Final Surge", "entity_id": "all", "type": "demand_surge"}
        ]
        
        for s in at_risk[:2]:
            scenarios.append({
                "id": f"risk_{s['supplier_id']}",
                "name": f"{s['name']} Failure (Risk: {s['risk_score']})",
                "entity_id": s["supplier_id"],
                "type": "supplier_failure"
            })
        
        return {"scenarios": scenarios}
