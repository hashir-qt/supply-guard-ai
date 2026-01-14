from typing import List, Optional, Dict
from sqlmodel import Session, select, col
from backend.models.schemas import (
    Supplier, Outlet, DeliveryRoute, Risk, RiskStatus, 
    CalendarEvent, HistoricalIncident, RiskSeverity
)

class DataService:
    def __init__(self, session: Session):
        self.session = session

    def get_suppliers(self) -> List[Supplier]:
        return self.session.exec(select(Supplier)).all()

    def get_outlets(self) -> List[Outlet]:
        return self.session.exec(select(Outlet)).all()
        
    def get_outlet(self, outlet_id: str) -> Optional[Outlet]:
        return self.session.get(Outlet, outlet_id)

    def get_active_risks(self) -> List[Risk]:
        return self.session.exec(
            select(Risk).where(Risk.status == RiskStatus.ACTIVE)
        ).all()
        
    def get_routes(self) -> List[DeliveryRoute]:
        return self.session.exec(select(DeliveryRoute)).all()
        
    def get_events(self) -> List[CalendarEvent]:
        return self.session.exec(select(CalendarEvent)).all()
        
    def get_history(self) -> List[HistoricalIncident]:
        return self.session.exec(select(HistoricalIncident)).all()

    def get_metric_summary(self) -> Dict:
        """Get high-level dashboard metrics."""
        suppliers = self.get_suppliers()
        outlets = self.get_outlets()
        risks = self.get_active_risks()
        
        critical_alerts = sum(1 for r in risks if r.severity == RiskSeverity.CRITICAL or r.risk_score > 70)
        
        # Calculate overall health score (mock logic based on active risks)
        base_score = 100
        deduction = sum(r.risk_score * 0.1 for r in risks)
        health_score = max(0, min(100, base_score - deduction))
        
        # Calculate at-risk outlets
        outlets_at_risk = sum(1 for o in outlets if o.current_risk_score > 50)
        
        # Get active deliveries (mocked for now as routes logic might be simple)
        routes = self.get_routes()
        active_deliveries = sum(1 for r in routes if r.current_status in ["on_route", "scheduled"])

        return {
            "total_suppliers": len(suppliers),
            "total_outlets": len(outlets),
            "active_risks": len(risks),
            "critical_alerts": critical_alerts,
            "overall_health_score": round(health_score, 1),
            "outlets_at_risk": outlets_at_risk,
            "active_deliveries": active_deliveries
        }

data = DataService(Session)
print(data.get_metric_summary())