"""Logistics Tools - Real route/delivery analysis from database"""
from sqlmodel import Session, select
from typing import Optional
from backend.models.schemas import DeliveryRoute

def analyze_delivery_routes(
    session: Session,
    route_id: Optional[str] = None,
    zone: Optional[str] = None,
    status_filter: Optional[str] = None
) -> dict:
    """Analyze delivery routes - REAL DATA"""
    
    query = select(DeliveryRoute)
    
    if route_id:
        route = session.get(DeliveryRoute, route_id)
        if not route:
            return {"error": f"Route {route_id} not found"}
        routes = [route]
    else:
        routes = session.exec(query).all()
    
    if zone:
        routes = [r for r in routes if zone.lower() in r.name.lower()]
    
    if status_filter:
        routes = [r for r in routes if r.current_status == status_filter]
    
    results = []
    for r in routes:
        metrics = r.metrics or {}
        schedule = r.schedule or {}
        
        results.append({
            "route_id": r.route_id,
            "name": r.name,
            "status": r.current_status,
            "origin": r.origin.get("name") if r.origin else "Unknown",
            "outlets_served": r.outlets_served or [],
            "metrics": {
                "distance_km": metrics.get("distance_km", 0),
                "on_time_rate": metrics.get("on_time_rate", 0)
            },
            "schedule": schedule,
            "is_delayed": r.current_status == "delayed"
        })
    
    # Summary stats
    total = len(results)
    delayed = len([r for r in results if r["is_delayed"]])
    active = len([r for r in results if r["status"] == "on_route"])
    
    return {
        "summary": {
            "total_routes": total,
            "delayed": delayed,
            "active": active,
            "on_time_rate": round((total - delayed) / total * 100, 1) if total > 0 else 100
        },
        "routes": results
    }

def get_delayed_routes(session: Session) -> dict:
    """Get all delayed routes - REAL DATA"""
    routes = session.exec(select(DeliveryRoute).where(DeliveryRoute.current_status == "delayed")).all()
    
    return {
        "total_delayed": len(routes),
        "routes": [
            {
                "route_id": r.route_id,
                "name": r.name,
                "outlets_affected": r.outlets_served or [],
                "origin": r.origin.get("name") if r.origin else "Unknown"
            }
            for r in routes
        ]
    }
