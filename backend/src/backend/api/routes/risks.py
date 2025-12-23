from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from backend.models.schemas import Risk
from backend.data.service import DataService
from backend.database import get_session

router = APIRouter()

def get_data_service(session: Session = Depends(get_session)) -> DataService:
    return DataService(session)

@router.get("/", response_model=List[Risk])
def get_risks(data: DataService = Depends(get_data_service)):
    return data.get_active_risks()

@router.get("/{risk_id}", response_model=Risk)
def get_risk_detail(risk_id: str, session: Session = Depends(get_session)):
    risk = session.get(Risk, risk_id)
    if not risk:
        raise HTTPException(status_code=404, detail="Risk not found")
    return risk
