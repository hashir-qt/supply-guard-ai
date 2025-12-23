from typing import List, Dict
from datetime import date, timedelta
from backend.models.schemas import CalendarEvent

class DemandPredictor:
    def forecast_demand(self, outlet_id: str, days: int = 7) -> List[Dict]:
        """Generate daily demand forecast for an outlet."""
        # Simple mock forecast
        base_demand = 450 # Avg daily orders
        forecasts = []
        today = date(2026, 1, 15) # Demo date
        
        for i in range(days):
            forecast_date = today + timedelta(days=i)
            # Add some variability
            noise = (i % 3) * 10
            daily_forecast = base_demand + noise
            
            forecasts.append({
                "date": forecast_date.isoformat(),
                "predicted_orders": daily_forecast,
                "confidence_interval": [daily_forecast - 20, daily_forecast + 20]
            })
            
        return forecasts

    def apply_event_multipliers(self, base_forecast: List[Dict], events: List[CalendarEvent]) -> List[Dict]:
        """Adjust forecast based on event impact multipliers."""
        adjusted_forecast = []
        
        for day_data in base_forecast:
            day_date = date.fromisoformat(day_data["date"])
            original_orders = day_data["predicted_orders"]
            final_orders = original_orders
            
            active_events = []
            
            for event in events:
                if event.start_date <= day_date <= event.end_date:
                    impact = event.impact_on_demand or {}
                    multiplier = impact.get("multiplier", 1.0)
                    
                    if impact.get("pattern") == "surge":
                        final_orders *= multiplier
                        active_events.append(event.name)
            
            day_data["adjusted_orders"] = int(final_orders)
            day_data["active_events"] = active_events
            adjusted_forecast.append(day_data)
            
        return adjusted_forecast

    def calculate_stockout_probability(self, current_inventory: dict, forecast: List[Dict]) -> float:
        """Calculate probability of stockout within the forecast period."""
        stock = current_inventory.get("frozen_chicken_kg", 0)
        kg_per_order = 0.5 # Approx 0.5kg per order
        
        total_demand_kg = sum(f.get("adjusted_orders", f["predicted_orders"]) for f in forecast) * kg_per_order
        
        if stock == 0:
            return 1.0
            
        coverage_ratio = stock / total_demand_kg if total_demand_kg > 0 else 100
        
        if coverage_ratio >= 1.2:
            return 0.05 # Low probability
        elif coverage_ratio >= 1.0:
            return 0.3 # Moderate
        elif coverage_ratio >= 0.8:
            return 0.7 # High
        else:
            return 0.95 # Critical
