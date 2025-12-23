"""Outlet Tools - Using OpenAI Agents SDK"""
from agents import function_tool
from sqlmodel import select
from typing import Optional

from backend.database import get_session
from backend.models.schemas import Outlet
from backend.data.enrichment import enrich_outlet, enrich_outlets

@function_tool
def check_outlet_status(
    outlet_id: Optional[str] = None,
    city: Optional[str] = None
) -> dict:
    """
    Check status of specific outlet(s).
    
    Args:
        outlet_id: e.g. "KHI-001" for KFC Clifton
        city: "Karachi", "Lahore", "Islamabad"
    
    Returns:
    - Outlet details with risk score
    - Inventory levels (chicken_days_remaining)
    - Recommendations
    
    Use when user asks:
    - "How's KFC Clifton?"
    - "Check Karachi outlets"
    - "Which outlets have problems?"
    """
    with next(get_session()) as session:
        if outlet_id:
            outlet = session.get(Outlet, outlet_id)
            if not outlet:
                return {"error": f"Outlet {outlet_id} not found"}
            outlets = [outlet]
        elif city:
            outlets = session.exec(select(Outlet).where(Outlet.city == city)).all()
        else:
            outlets = session.exec(select(Outlet)).all()
        
        if not outlets:
            return {"error": "No outlets found"}
        
        enriched = enrich_outlets(outlets)
        
        results = []
        for o in enriched:
            inv = o.get("inventory", {}) or {}
            days = inv.get("chicken_days_remaining", 99)
            
            status = "critical" if days < 2 else "warning" if days < 3 else "healthy"
            
            recs = []
            if days < 1.5:
                recs.append("CRITICAL: Emergency delivery within 12 hours")
            elif days < 2:
                recs.append("Schedule urgent delivery within 24 hours")
            elif days < 3:
                recs.append("Schedule delivery within 48 hours")
            
            results.append({
                "outlet_id": o["outlet_id"],
                "name": o["name"],
                "city": o["city"],
                "risk_score": o["current_risk_score"],
                "chicken_days_remaining": days,
                "inventory_status": status,
                "recommendations": recs if recs else ["Operating normally"]
            })
        
        results = sorted(results, key=lambda x: x["risk_score"], reverse=True)
        return results[0] if len(results) == 1 else {"outlets": results}

@function_tool
def get_low_inventory_outlets(threshold: float = 2.0) -> dict:
    """
    Get outlets with critically low chicken inventory.
    
    Args:
        threshold: days of inventory (default 2.0)
    
    Use when user asks:
    - "Which outlets are running low?"
    - "Low inventory outlets"
    - "Chicken shortage where?"
    """
    with next(get_session()) as session:
        outlets = session.exec(select(Outlet)).all()
        
        low_stock = []
        for o in outlets:
            inv = o.inventory or {}
            days = inv.get("chicken_days_remaining", 99)
            if days < threshold:
                enriched = enrich_outlet(o)
                low_stock.append({
                    "outlet_id": o.outlet_id,
                    "name": o.name,
                    "city": o.city,
                    "chicken_days": days,
                    "status": "critical" if days < 1.5 else "warning"
                })
        
        low_stock = sorted(low_stock, key=lambda x: x["chicken_days"])
        
        return {
            "total_low_stock": len(low_stock),
            "threshold_days": threshold,
            "outlets": low_stock
        }
