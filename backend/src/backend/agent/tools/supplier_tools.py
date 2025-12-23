"""Supplier Tools - Using OpenAI Agents SDK"""
from agents import function_tool
from sqlmodel import Session, select
from typing import Optional

from backend.database import get_session
from backend.models.schemas import Supplier, Risk
from backend.data.enrichment import enrich_supplier, enrich_suppliers

@function_tool
def analyze_supplier_risk(
    supplier_id: Optional[str] = None,
    supplier_name: Optional[str] = None
) -> dict:
    """
    Analyze risk for specific supplier(s).
    
    Args:
        supplier_id: e.g. "SUP-001" for K&N's
        supplier_name: partial name match e.g. "K&N" or "Malik"
    
    Returns:
    - Supplier details with calculated risk_score
    - Risk breakdown by factor
    - Active alerts
    - Alternative suppliers
    - Specific recommendations
    
    Use when user asks:
    - "What's the risk with K&N's?"
    - "Analyze Malik Farms"
    - "Which suppliers are risky?"
    """
    with next(get_session()) as session:
        if supplier_id:
            supplier = session.get(Supplier, supplier_id)
            if not supplier:
                return {"error": f"Supplier {supplier_id} not found"}
            suppliers = [supplier]
        elif supplier_name:
            all_suppliers = session.exec(select(Supplier)).all()
            suppliers = [s for s in all_suppliers if supplier_name.lower() in s.name.lower()]
        else:
            suppliers = session.exec(select(Supplier)).all()
        
        if not suppliers:
            return {"error": "No suppliers found"}
        
        enriched = enrich_suppliers(suppliers)
        
        results = []
        for s in enriched:
            metrics = s.get("metrics", {}) or {}
            risk_factors = s.get("risk_factors", {}) or {}
            
            # Find alternatives
            all_sups = session.exec(select(Supplier)).all()
            alternatives = [
                a for a in enrich_suppliers(all_sups)
                if a["supplier_id"] != s["supplier_id"]
            ][:3]
            
            results.append({
                "supplier_id": s["supplier_id"],
                "name": s["name"],
                "risk_score": s["risk_score"],
                "status": s["current_status"],
                "city": s.get("location", {}).get("city") if s.get("location") else "Unknown",
                "metrics": metrics,
                "active_alerts": s.get("active_alerts", []),
                "alternatives": [{"name": a["name"], "risk_score": a["risk_score"]} for a in alternatives],
                "recommendations": _get_supplier_recs(s)
            })
        
        return results[0] if len(results) == 1 else {"suppliers": results}

def _get_supplier_recs(s):
    recs = []
    if s["risk_score"] >= 70:
        recs.append("URGENT: Contact backup suppliers immediately")
    if s.get("active_alerts"):
        recs.append(f"Investigate alerts: {', '.join(s['active_alerts'])}")
    metrics = s.get("metrics", {}) or {}
    if metrics.get("reliability", 100) < 90:
        recs.append(f"Address reliability issues (currently {metrics.get('reliability')}%)")
    return recs if recs else ["Supplier performing well"]

@function_tool
def get_at_risk_suppliers(threshold: int = 50) -> dict:
    """
    Get all suppliers above risk threshold.
    
    Args:
        threshold: minimum risk score (default 50)
    
    Use when user asks:
    - "Which suppliers are at risk?"
    - "Show high risk suppliers"
    """
    with next(get_session()) as session:
        suppliers = session.exec(select(Supplier)).all()
        enriched = enrich_suppliers(suppliers)
        at_risk = [s for s in enriched if s["risk_score"] >= threshold]
        at_risk = sorted(at_risk, key=lambda x: x["risk_score"], reverse=True)
        
        return {
            "total_at_risk": len(at_risk),
            "threshold": threshold,
            "suppliers": [
                {"supplier_id": s["supplier_id"], "name": s["name"], "risk_score": s["risk_score"], "alerts": s.get("active_alerts", [])}
                for s in at_risk
            ]
        }
