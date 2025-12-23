from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from backend.database import get_session
from backend.models.schemas import Supplier, SupplierType

router = APIRouter()

@router.get("/", response_model=List[Supplier])
def get_all_suppliers(
    supplier_type: Optional[SupplierType] = None,
    session: Session = Depends(get_session)
):
    query = select(Supplier)
    if supplier_type:
        query = query.where(Supplier.type == supplier_type)
    return session.exec(query).all()

@router.get("/at-risk", response_model=List[Supplier])
def get_at_risk_suppliers(
    threshold: int = Query(50),
    session: Session = Depends(get_session)
):
    return session.exec(select(Supplier).where(Supplier.risk_score >= threshold)).all()

from backend.services.analysis_service import generate_supplier_analysis

@router.get("/{supplier_id}", response_model=Supplier)
async def get_supplier_detail(
    supplier_id: str, 
    include_analysis: bool = False,
    session: Session = Depends(get_session)
):
    supplier = session.get(Supplier, supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
        
    if include_analysis:
        # Generate analysis on fly
        analysis = await generate_supplier_analysis(supplier.model_dump())
        supplier.ai_analysis = analysis
        
    return supplier
