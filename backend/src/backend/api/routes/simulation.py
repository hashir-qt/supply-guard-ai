from fastapi import APIRouter, Depends
from backend.models.schemas import SimulationRequest, SimulationResult
from backend.services.cascade_simulator import CascadeSimulator

router = APIRouter()

def get_simulator() -> CascadeSimulator:
    return CascadeSimulator()

@router.post("/run", response_model=SimulationResult)
def run_simulation(
    request: SimulationRequest,
    simulator: CascadeSimulator = Depends(get_simulator)
):
    # Simple simulation logic
    result = simulator.simulate_disruption(
        request.disruption_type, 
        request.severity, 
        request.duration_days
    )
    
    # Calculate impacts
    outlets_count = 15 # Mocked for demo based on result timeline
    revenue_loss = simulator.estimate_revenue_impact(outlets_count, request.duration_days)
    
    return SimulationResult(
        scenario_id="SIM-001",
        timeline=result["timeline"],
        impact_summary={
            "revenue_at_risk": revenue_loss,
            "outlets_affected": outlets_count,
            "inventory_shortfall_kg": 2500
        },
        recommendations=["Increase buffer stock", "Activate backup supplier"]
    )
