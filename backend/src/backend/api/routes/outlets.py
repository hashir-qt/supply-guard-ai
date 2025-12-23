from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from backend.database import get_session
from backend.models.schemas import Outlet

router = APIRouter()

@router.get("/", response_model=List[Outlet])
def get_all_outlets(
    city: Optional[str] = None,
    session: Session = Depends(get_session)
):
    query = select(Outlet)
    if city:
        query = query.where(Outlet.city == city)
    return session.exec(query).all()

@router.get("/low-inventory", response_model=List[Outlet])
def get_low_inventory_outlets(
    threshold: float = Query(2.0),
    session: Session = Depends(get_session)
):
    # Depending on schema, this might need a join or direct field check.
    # Assuming Outlet has a field 'days_inventory_remaining' temporarily for MVP
    # If not, we might need to rely on populated data field matching Pydantic model
    return session.exec(select(Outlet).where(Outlet.chicken_days_remaining <= threshold)).all()

@router.get("/{outlet_id}", response_model=Outlet)
def get_outlet_detail(outlet_id: str, session: Session = Depends(get_session)):
    outlet = session.get(Outlet, outlet_id)
    if not outlet:
        raise HTTPException(status_code=404, detail="Outlet not found")
    return outlet
