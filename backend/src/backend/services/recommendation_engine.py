from typing import List, Dict
from backend.models.schemas import Risk, RiskRecommendation, Supplier

class RecommendationEngine:
    def generate_recommendations(self, risk: Risk) -> List[RiskRecommendation]:
        """Generate prioritized recommendations based on risk context."""
        recommendations = []
        
        if risk.category == "supplier" and risk.severity == "critical":
            recommendations.append(RiskRecommendation(
                action="Activate secondary supplier (K&N's Karachi)",
                priority=1,
                effort="low",
                impact="high",
                deadline="Immediate"
            ))
            recommendations.append(RiskRecommendation(
                action="Reduce menu to core items at Lahore outlets",
                priority=2,
                effort="medium",
                impact="medium"
            ))
        elif risk.category == "demand" and "PSL" in risk.title:
             recommendations.append(RiskRecommendation(
                action="Increase chicken inventory bu 30% at Stadium outlets",
                priority=1,
                effort="medium",
                impact="high"
            ))
             recommendations.append(RiskRecommendation(
                 action="Schedule extra delivery run",
                 priority=2,
                 effort="high",
                 impact="high"
             ))
        
        return recommendations

    def optimize_inventory(self, outlet_id: str, current_stock: float, risk_factor: float) -> float:
        """Calculate optimal inventory level."""
        base_stock = 100 # kg
        return base_stock * (1 + risk_factor)

    def find_alternative_suppliers(self, current_supplier_id: str, all_suppliers: List[Supplier]) -> List[Supplier]:
        """Find suitable backup suppliers."""
        # Mock logic: return any tier 1 supplier different from current
        return [s for s in all_suppliers if s.supplier_id != current_supplier_id and s.category == "tier_1"]
