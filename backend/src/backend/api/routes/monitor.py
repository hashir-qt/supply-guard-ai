"""
Monitoring API - Trigger risk detection manually (for demo)
In production, these would run via Celery every 15 minutes
"""
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from typing import List

from backend.database import get_session
from backend.models.schemas import Supplier, Outlet, Risk
from backend.services.monitors import SupplierHealthMonitor, OutletInventoryMonitor, AlertGenerator

router = APIRouter()

@router.post("/check-all")
async def run_full_monitoring_cycle(session: Session = Depends(get_session)):
    """
    Run complete monitoring cycle - checks all suppliers and outlets.
    In production: This runs automatically every 15 minutes via Celery.
    For demo: Trigger manually to show real-time risk detection.
    """
    
    # Initialize monitors
    supplier_monitor = SupplierHealthMonitor()
    outlet_monitor = OutletInventoryMonitor()
    alert_generator = AlertGenerator()
    
    # Get all data
    suppliers = session.exec(select(Supplier)).all()
    outlets = session.exec(select(Outlet)).all()
    
    # Run checks
    supplier_issues = supplier_monitor.check_all_suppliers(suppliers, session)
    outlet_issues = outlet_monitor.check_all_outlets(outlets, session)
    
    all_issues = supplier_issues + outlet_issues
    
    # Generate alerts
    created_risks = alert_generator.generate_alerts(all_issues, session)
    
    return {
        "status": "monitoring_complete",
        "checks_performed": {
            "suppliers_checked": len(suppliers),
            "outlets_checked": len(outlets)
        },
        "issues_detected": len(all_issues),
        "alerts_created": len(created_risks),
        "new_risks": [
            {
                "risk_id": r.risk_id,
                "title": r.title,
                "severity": r.severity,
                "category": r.category
            }
            for r in created_risks
        ]
    }

@router.post("/check-suppliers")
async def check_suppliers_only(session: Session = Depends(get_session)):
    """Check only supplier health"""
    monitor = SupplierHealthMonitor()
    alert_gen = AlertGenerator()
    
    suppliers = session.exec(select(Supplier)).all()
    issues = monitor.check_all_suppliers(suppliers, session)
    risks = alert_gen.generate_alerts(issues, session)
    
    return {
        "suppliers_checked": len(suppliers),
        "issues_found": len(issues),
        "alerts_created": len(risks),
        "risks": [r.risk_id for r in risks]
    }

@router.post("/check-inventory")
async def check_inventory_only(session: Session = Depends(get_session)):
    """Check only outlet inventory levels"""
    monitor = OutletInventoryMonitor()
    alert_gen = AlertGenerator()
    
    outlets = session.exec(select(Outlet)).all()
    issues = monitor.check_all_outlets(outlets, session)
    risks = alert_gen.generate_alerts(issues, session)
    
    return {
        "outlets_checked": len(outlets),
        "low_stock_alerts": len(issues),
        "alerts_created": len(risks),
        "critical_outlets": [
            i.get("outlet_id") for i in issues 
            if i.get("severity") == "critical"
        ]
    }

@router.get("/status")
async def get_monitoring_status(session: Session = Depends(get_session)):
    """Get current monitoring system status"""
    
    # Count active risks
    active_risks = session.exec(
        select(Risk).where(Risk.status == "active")
    ).all()
    
    return {
        "monitoring_active": True,
        "last_check": "Manual trigger (demo mode)",
        "active_alerts": len(active_risks),
        "next_scheduled_check": "Every 15 min in production",
        "status": "Demo Mode - Trigger via POST /api/monitor/check-all"
    }
