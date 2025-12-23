from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from backend.database import get_session
from backend.models.schemas import DeliveryRoute

router = APIRouter()

@router.get("/", response_model=List[DeliveryRoute])
def get_all_routes(
    status: Optional[str] = None,
    session: Session = Depends(get_session)
):
    query = select(DeliveryRoute)
    if status:
        query = query.where(DeliveryRoute.current_status == status)
    return session.exec(query).all()

@router.get("/delayed", response_model=List[DeliveryRoute])
def get_delayed_routes(session: Session = Depends(get_session)):
    # Assuming 'DELAYED' is a status in the enum or string field
    return session.exec(select(DeliveryRoute).where(DeliveryRoute.current_status == "DELAYED")).all()

@router.get("/{route_id}", response_model=DeliveryRoute)
def get_route_detail(route_id: str, session: Session = Depends(get_session)):
    route = session.exec(select(DeliveryRoute).where(DeliveryRoute.route_id == route_id)).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    return route
