from fastapi import APIRouter, Depends
from backend.models.schemas import SupplyChainOverview
from backend.data.service import DataService
from backend.database import get_session
from sqlmodel import Session

router = APIRouter()

def get_data_service(session: Session = Depends(get_session)) -> DataService:
    return DataService(session)

@router.get("/overview", response_model=SupplyChainOverview)
def get_overview(data: DataService = Depends(get_data_service)):
    metrics = data.get_metric_summary()
    return SupplyChainOverview(
        total_suppliers=metrics["total_suppliers"],
        total_outlets=metrics["total_outlets"],
        active_risks=metrics["active_risks"],
        overall_health_score=metrics["overall_health_score"],
        critical_alerts=metrics["critical_alerts"]
    )
