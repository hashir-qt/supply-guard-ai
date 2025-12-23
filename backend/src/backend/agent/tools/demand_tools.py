"""Demand & External Tools - Using OpenAI Agents SDK"""
from agents import function_tool
from sqlmodel import select
from typing import Optional
from datetime import date, timedelta

from backend.database import get_session
from backend.models.schemas import Outlet, CalendarEvent
from backend.data.enrichment import enrich_outlets

@function_tool
def forecast_demand(
    outlet_id: Optional[str] = None,
    city: Optional[str] = None,
    horizon_days: int = 30
) -> dict:
    """
    Forecast demand considering upcoming events.
    
    Args:
        outlet_id: specific outlet or None for all
        city: filter by city
        horizon_days: forecast window (default 30)
    
    Returns:
    - Upcoming events with demand multipliers
    - Stockout risks
    - Recommendations
    
    Use when user asks:
    - "What's demand for PSL final?"
    - "Forecast next week"
    - "How will Ramadan affect us?"
    """
    with next(get_session()) as session:
        # Get outlets
        if outlet_id:
            outlets = [session.get(Outlet, outlet_id)]
        elif city:
            outlets = session.exec(select(Outlet).where(Outlet.city == city)).all()
        else:
            outlets = session.exec(select(Outlet)).all()
        
        outlets = [o for o in outlets if o]
        
        # Get events
        today = date.today()
        events = session.exec(select(CalendarEvent)).all()
        upcoming = [e for e in events if e.start_date and today <= e.start_date <= today + timedelta(days=horizon_days)]
        
        base_demand = 150  # orders/day/outlet
        
        event_impacts = []
        for e in upcoming:
            impact = e.impact_on_demand or {}
            mult = impact.get("multiplier", 1.0)
            event_impacts.append({
                "event": e.name,
                "date": str(e.start_date),
                "days_until": (e.start_date - today).days,
                "demand_multiplier": mult,
                "expected_demand": int(base_demand * mult)
            })
        
        # Check stockout risks
        enriched = enrich_outlets(outlets)
        stockout_risks = []
        for o in enriched:
            inv = o.get("inventory", {}) or {}
            days = inv.get("chicken_days_remaining", 99)
            at_risk = any(e["days_until"] <= days for e in event_impacts if e["demand_multiplier"] > 1.5)
            if days < 3 or at_risk:
                stockout_risks.append({"outlet": o["name"], "days_remaining": days, "at_risk_for_event": at_risk})
        
        return {
            "outlets_analyzed": len(outlets),
            "forecast_days": horizon_days,
            "base_demand_per_outlet": base_demand,
            "upcoming_events": event_impacts,
            "stockout_risks": stockout_risks,
            "recommendations": [f"Prepare for {e['event']} in {e['days_until']} days" for e in event_impacts if e["demand_multiplier"] >= 2]
        }

@function_tool
def check_external_risks(risk_type: Optional[str] = None) -> dict:
    """
    Check external factors: events, weather impact.
    
    Args:
        risk_type: "religious", "sports", "weather", or None for all
    
    Use when user asks:
    - "Any upcoming events?"
    - "What external risks?"
    - "When's Ramadan?"
    """
    with next(get_session()) as session:
        today = date.today()
        events = session.exec(select(CalendarEvent)).all()
        upcoming = [e for e in events if e.start_date and e.start_date >= today]
        
        categorized = {"religious": [], "sports": [], "holiday": [], "weather": [], "other": []}
        
        for e in upcoming:
            etype = e.type if e.type else "other"
            entry = {
                "name": e.name,
                "date": str(e.start_date),
                "days_until": (e.start_date - today).days,
                "risk_level": e.risk_level,
                "demand_impact": e.impact_on_demand
            }
            if etype in categorized:
                categorized[etype].append(entry)
            else:
                categorized["other"].append(entry)
        
        if risk_type and risk_type in categorized:
            return {risk_type: categorized[risk_type]}
        
        urgent = [e for cat in categorized.values() for e in cat if e["days_until"] <= 7]
        return {"external_risks": categorized, "urgent_next_7_days": urgent}
