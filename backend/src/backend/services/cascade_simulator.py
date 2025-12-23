from typing import List, Dict
from datetime import date, timedelta
from backend.models.schemas import Risk, CascadeStage

class CascadeSimulator:
    def simulate_disruption(self, disruption_type: str, severity: str, duration_days: int) -> Dict:
        """Simulate how a disruption cascades over time."""
        stages = []
        
        # Mock logic based on type/severity
        if disruption_type == "supplier_failure" and severity == "critical":
            stages = [
                {"day": 1, "impact": "Supplier production halts", "outlets_affected": 0},
                {"day": 3, "impact": "Hub inventory depleted", "outlets_affected": 5},
                {"day": 7, "impact": "Stockouts at high-volume outlets", "outlets_affected": 12},
                {"day": 14, "impact": "Zone-wide menu restrictions", "outlets_affected": 30}
            ]
        elif disruption_type == "demand_surge":
            stages = [
                {"day": 0, "impact": "Event start", "outlets_affected": 0},
                {"day": 1, "impact": "Rapid stock depletion", "outlets_affected": 8},
                {"day": 2, "impact": "Emergency deliveries required", "outlets_affected": 15}
            ]
        else:
             stages = [
                {"day": 1, "impact": "Initial impact monitoring", "outlets_affected": 0},
                {"day": duration_days, "impact": "Projected resolution", "outlets_affected": 2}
            ]
            
        return {
            "disruption_type": disruption_type,
            "severity": severity,
            "duration": duration_days,
            "timeline": stages
        }

    def calculate_affected_outlets(self, risk: Risk, day_offset: int = 0) -> List[str]:
        """Identify which outlets will be affected at a given point in the cascade."""
        # Simple mock logic: if risk is supplier-based, affect outlets served by that supplier
        # For now, return hardcoded demo data based on risk ID
        if "Lahore" in risk.title:
            return ["LHR-001", "LHR-002", "LHR-003", "LHR-004", "LHR-005"]
        elif "Karachi" in risk.title or "KFC Clifton" in risk.description:
             return ["KHI-001", "KHI-002", "KHI-007"]
        return []

    def estimate_revenue_impact(self, affected_outlets_count: int, duration_days: int) -> int:
        """Estimate PKR revenue impact."""
        avg_daily_revenue_per_outlet = 150000 # 1.5 Lakh PKR
        return affected_outlets_count * avg_daily_revenue_per_outlet * duration_days
