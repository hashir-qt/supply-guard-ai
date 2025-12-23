"""
Helper functions to add computed fields to database models.
These calculate risk scores dynamically from base data.
"""
from backend.models.schemas import Supplier, Outlet
from backend.services.risk_scorer import RiskScorer

scorer = RiskScorer()

def enrich_supplier(supplier: Supplier) -> dict:
    """Add computed risk_score and status to supplier."""
    risk_score = scorer.calculate_supplier_risk(supplier)
    
    # Derive status from risk score
    if risk_score >= 70:
        status = "critical"
    elif risk_score >= 50:
        status = "warning"
    else:
        status = "operational"  
    
    return {
        **supplier.model_dump(),
        "risk_score": round(risk_score, 1),
        "current_status": status
    }

def enrich_outlet(outlet: Outlet) -> dict:
    """Add computed risk_score to outlet."""
    risk_score = scorer.calculate_outlet_risk(outlet)
    
    return {
        **outlet.model_dump(),
        "current_risk_score": round(risk_score, 1)
    }

def enrich_suppliers(suppliers: list[Supplier]) -> list[dict]:
    """Enrich multiple suppliers."""
    return [enrich_supplier(s) for s in suppliers]

def enrich_outlets(outlets: list[Outlet]) -> list[dict]:
    """Enrich multiple outlets."""
    return [enrich_outlet(o) for o in outlets]
