from typing import List, Optional
from sqlmodel import Session
from backend.models.schemas import Risk, RiskStatus

class AlertManager:
    def __init__(self, session: Session):
        self.session = session

    def create_alert(self, risk: Risk) -> Risk:
        """Create a new risk alert in the system."""
        self.session.add(risk)
        self.session.commit()
        self.session.refresh(risk)
        return risk

    def update_alert_status(self, risk_id: str, status: RiskStatus):
        """Update the status of an existing alert."""
        risk = self.session.get(Risk, risk_id)
        if risk:
            risk.status = status
            self.session.add(risk)
            self.session.commit()

    def get_active_alerts(self) -> List[Risk]:
        """Get all currently active alerts."""
        # This logic is also in DataService, but specific alert logic can go here
        from sqlmodel import select
        return self.session.exec(select(Risk).where(Risk.status == RiskStatus.ACTIVE)).all()
