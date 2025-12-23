"""Recommendation & History Tools - Using OpenAI Agents SDK"""
from agents import function_tool
from sqlmodel import select
from typing import Optional

from backend.database import get_session
from backend.models.schemas import Risk, Supplier, Outlet, HistoricalIncident
from backend.data.enrichment import enrich_suppliers

@function_tool
def get_recommendations(
    risk_id: Optional[str] = None,
    category: Optional[str] = None,
    top_n: int = 5
) -> dict:
    """
    Get prioritized actionable recommendations.
    
    Args:
        risk_id: recommendations for specific risk
        category: "supplier", "logistics", "demand"
        top_n: number of recommendations
    
    Use when user asks:
    - "What should we do?"
    - "Give me recommendations"
    - "How do we fix this?"
    """
    with next(get_session()) as session:
        recommendations = []
        
        # Get at-risk suppliers
        suppliers = session.exec(select(Supplier)).all()
        enriched = enrich_suppliers(suppliers)
        for s in enriched:
            if s["risk_score"] >= 70:
                recommendations.append({
                    "action": f"URGENT: Contact backup for {s['name']} (risk: {s['risk_score']})",
                    "priority": 1,
                    "source": s["supplier_id"],
                    "deadline": "Within 24 hours"
                })
            elif s["risk_score"] >= 50:
                recommendations.append({
                    "action": f"Review {s['name']} and develop contingency",
                    "priority": 2,
                    "source": s["supplier_id"],
                    "deadline": "Within 1 week"
                })
        
        # Check low inventory
        outlets = session.exec(select(Outlet)).all()
        for o in outlets:
            inv = o.inventory or {}
            days = inv.get("chicken_days_remaining", 99)
            if days < 2.0:
                recommendations.append({
                    "action": f"Emergency delivery to {o.name} ({days:.1f} days left)",
                    "priority": 1,
                    "source": o.outlet_id,
                    "deadline": "Within 12 hours"
                })
        
        # Add from active risks
        risks = session.exec(select(Risk).where(Risk.status == "active")).all()
        for r in sorted(risks, key=lambda x: x.risk_score, reverse=True)[:3]:
            if r.recommendations:
                for rec in r.recommendations[:1]:
                    recommendations.append({
                        "action": rec.get("action", f"Address {r.title}"),
                        "priority": rec.get("priority", 2),
                        "source": r.risk_id
                    })
        
        recommendations = sorted(recommendations, key=lambda x: x.get("priority", 5))[:top_n]
        return {"total": len(recommendations), "recommendations": recommendations}

@function_tool
def get_historical_incidents(incident_type: Optional[str] = None) -> dict:
    """
    Get past incidents with lessons learned.
    
    Args:
        incident_type: "weather_flooding", "supplier_outage", etc.
    
    Use when user asks:
    - "Past incidents?"
    - "What happened before?"
    - "Historical problems?"
    """
    with next(get_session()) as session:
        query = select(HistoricalIncident)
        if incident_type:
            query = query.where(HistoricalIncident.type == incident_type)
        
        incidents = session.exec(query).all()
        
        return {
            "total": len(incidents),
            "incidents": [
                {
                    "date": str(i.date),
                    "type": i.type,
                    "description": i.description,
                    "duration_days": i.duration_days,
                    "impact": i.impact,
                    "lessons_learned": i.lessons_learned
                }
                for i in incidents
            ]
        }
