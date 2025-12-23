from fastapi import APIRouter
from backend.models.schemas import DemandForecast

router = APIRouter()

@router.get("/demand/{outlet_id}", response_model=DemandForecast)
def get_demand_forecast(outlet_id: str):
    # Stub implementation. 
    # Real implementation would call DemandPredictor service.
    return DemandForecast(
        outlet_id=outlet_id,
        forecast_date="2025-02-15",
        predicted_orders=450,
        confidence_score=0.85,
        influencing_factors=["Weekend", "No Events"]
    )
