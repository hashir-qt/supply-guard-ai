"""Overview Tools - Using OpenAI Agents SDK"""
from agents import function_tool
from sqlmodel import Session, select
from datetime import date, timedelta

from backend.database import get_session
from backend.models.schemas import Supplier, Outlet, Risk, CalendarEvent
from backend.data.enrichment import enrich_suppliers, enrich_outlets

@function_tool
def get_supply_chain_overview() -> dict:
    """
    Get comprehensive overview of KFC Pakistan's supply chain health.
    
    Returns:
    - overall_risk_score: 0-100 aggregate risk
    - total_outlets: number of outlets
    - outlets_at_risk: outlets with risk > 50
    - active_alerts: number of active risk alerts
    - category_scores: {supplier, logistics, demand, external}
    - top_risks: Top 5 highest priority risks
    - upcoming_events: Events in next 60 days
    
    Use when user asks:
    - "How's our supply chain?"
    - "Give me an overview"
    - "What's the overall status?"
    """
    with next(get_session()) as session:
        # Get real data from DB
        suppliers = session.exec(select(Supplier)).all()
        outlets = session.exec(select(Outlet)).all()
        risks = session.exec(select(Risk).where(Risk.status == "active")).all()
        events = session.exec(select(CalendarEvent)).all()
        
        # Enrich with calculated risk scores
        enriched_suppliers = enrich_suppliers(suppliers)
        enriched_outlets = enrich_outlets(outlets)
        
        # Calculate metrics
        avg_supplier_risk = sum(s["risk_score"] for s in enriched_suppliers) / len(enriched_suppliers) if enriched_suppliers else 0
        avg_outlet_risk = sum(o["current_risk_score"] for o in enriched_outlets) / len(enriched_outlets) if enriched_outlets else 0
        
        outlets_at_risk = len([o for o in enriched_outlets if o["current_risk_score"] >= 50])
        suppliers_at_risk = len([s for s in enriched_suppliers if s["risk_score"] >= 50])
        
        # Category breakdown
        supplier_risks = [r for r in risks if r.category == "supplier"]
        logistics_risks = [r for r in risks if r.category == "logistics"]
        demand_risks = [r for r in risks if r.category == "demand"]
        external_risks = [r for r in risks if r.category == "external"]
        
        # Upcoming events
        today = date.today()
        upcoming = [e for e in events if e.start_date and e.start_date >= today and e.start_date <= today + timedelta(days=60)]
        
        # Top 5 risks
        top_risks = sorted(risks, key=lambda r: r.risk_score, reverse=True)[:5]
        
        return {
            "overall_risk_score": round((avg_supplier_risk + avg_outlet_risk) / 2, 1),
            "total_outlets": len(outlets),
            "total_suppliers": len(suppliers),
            "outlets_at_risk": outlets_at_risk,
            "suppliers_at_risk": suppliers_at_risk,
            "active_alerts": len(risks),
            "category_scores": {
                "supplier": round(avg_supplier_risk, 1),
                "logistics": round(sum(r.risk_score for r in logistics_risks) / max(len(logistics_risks), 1), 1),
                "demand": round(sum(r.risk_score for r in demand_risks) / max(len(demand_risks), 1), 1),
                "external": round(sum(r.risk_score for r in external_risks) / max(len(external_risks), 1), 1)
            },
            "top_risks": [
                {"risk_id": r.risk_id, "title": r.title, "severity": r.severity, "risk_score": r.risk_score}
                for r in top_risks
            ],
            "upcoming_events": [
                {"name": e.name, "days_until": (e.start_date - today).days, "risk_level": e.risk_level}
                for e in upcoming
            ]
        }
