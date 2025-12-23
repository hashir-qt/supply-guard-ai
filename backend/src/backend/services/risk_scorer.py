from backend.models.schemas import Supplier, Outlet, RiskCategory

class RiskScorer:
    def calculate_supplier_risk(self, supplier: Supplier) -> float:
        """Calculate risk score (0-100) for a supplier based on metrics and risk factors."""
        score = 50.0 # Base score (medium risk)
        
        # Adjust based on metrics
        metrics = supplier.metrics
        if metrics:
            reliability = metrics.get("reliability_score", metrics.get("reliability", 80))
            quality = metrics.get("quality_score", metrics.get("quality", 80))
            
            # Lower reliability = Higher risk
            score += (100 - reliability) * 0.5
            # Lower quality = Higher risk
            score += (100 - quality) * 0.3
            
        # Adjust based on risk factors
        factors = supplier.risk_factors
        if factors:
            if factors.get("single_source"):
                score += 15
            if factors.get("financial_health") == "unstable":
                score += 20
            if factors.get("geographic_risk") == "high":
                score += 15
                
        # Adjust based on active alerts
        if supplier.active_alerts:
            score += len(supplier.active_alerts) * 10
            
        return min(max(score, 0), 100)

    def calculate_outlet_risk(self, outlet: Outlet) -> float:
        """Calculate risk score for an outlet based on inventory and sales."""
        score = 20.0 # Base low risk
        
        inventory = outlet.inventory
        if inventory:
            days_remaining = inventory.get("chicken_days_remaining", 5.0)
            if days_remaining < 2.0:
                score += 50 # Critical stock level
            elif days_remaining < 3.0:
                score += 30
            elif days_remaining < 4.0:
                score += 10
                
        equipment = outlet.equipment_status
        if equipment:
            if equipment.get("freezer_temp", -18) > -10:
                score += 40 # Critical equipment failure
            if equipment.get("generator_fuel_pct", 100) < 30:
                score += 10
                
        return min(max(score, 0), 100)

    def get_category_scores(self) -> dict:
        """Get aggregate risk scores by category (Mock logic for MVP)."""
        return {
            RiskCategory.SUPPLIER: 67,
            RiskCategory.LOGISTICS: 45,
            RiskCategory.DEMAND: 82,
            RiskCategory.EXTERNAL: 58
        }
