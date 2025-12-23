"""
Risk Detection Monitors - Analyze data and auto-create alerts
"""
from datetime import datetime, date
from typing import List
from sqlmodel import Session

from backend.models.schemas import Supplier, Outlet, Risk, RiskSeverity, RiskCategory, RiskStatus
from backend.data.enrichment import enrich_supplier, enrich_outlet

class SupplierHealthMonitor:
    """Monitors supplier metrics and detects deteriorating performance"""
    
    def check_supplier(self, supplier: Supplier, session: Session) -> List[dict]:
        """Check single supplier for risks"""
        alerts = []
        enriched = enrich_supplier(supplier)
        risk_score = enriched["risk_score"]
        
        # Check 1: High risk score
        if risk_score > 70:
            alerts.append({
                "type": "high_risk_score",
                "severity": RiskSeverity.CRITICAL,
                "title": f"{supplier.name} - Critical Risk Score",
                "description": f"Supplier risk score at {risk_score}. Immediate action required.",
                "supplier_id": supplier.supplier_id
            })
        
        # Check 2: Low reliability
        metrics = supplier.metrics or {}
        reliability = metrics.get("reliability", metrics.get("reliability_score", 100))
        if reliability < 85:
            alerts.append({
                "type": "low_reliability",
                "severity": RiskSeverity.HIGH,
                "title": f"{supplier.name} - Reliability Drop",
                "description": f"On-time delivery dropped to {reliability}% (threshold: 85%)",
                "supplier_id": supplier.supplier_id
            })
        
        # Check 3: Active disease alerts
        if supplier.active_alerts and any("flu" in alert.lower() or "disease" in alert.lower() for alert in supplier.active_alerts):
            alerts.append({
                "type": "disease_outbreak",
                "severity": RiskSeverity.CRITICAL,
                "title": f"{supplier.name} - Disease Alert",
                "description": f"Disease-related issues detected: {', '.join(supplier.active_alerts)}",
                "supplier_id": supplier.supplier_id
            })
        
        return alerts
    
    def check_all_suppliers(self, suppliers: List[Supplier], session: Session) -> List[dict]:
        """Check all suppliers and return detected risks"""
        all_alerts = []
        for supplier in suppliers:
            alerts = self.check_supplier(supplier, session)
            all_alerts.extend(alerts)
        return all_alerts


class OutletInventoryMonitor:
    """Monitors outlet inventory levels and detects stockout risks"""
    
    def check_outlet(self, outlet: Outlet, session: Session) -> List[dict]:
        """Check outlet for inventory risks"""
        alerts = []
        inventory = outlet.inventory or {}
        chicken_days = inventory.get("chicken_days_remaining", 10)
        
        # Critical: Less than 2 days
        if chicken_days < 2.0:
            alerts.append({
                "type": "critical_inventory",
                "severity": RiskSeverity.CRITICAL,
                "title": f"{outlet.name} - Critical Chicken Stock",
                "description": f"Only {chicken_days:.1f} days of chicken remaining. Stockout imminent.",
                "outlet_id": outlet.outlet_id,
                "chicken_days": chicken_days
            })
        # Warning: Less than 3 days
        elif chicken_days < 3.0:
            alerts.append({
                "type": "low_inventory",
                "severity": RiskSeverity.HIGH,
                "title": f"{outlet.name} - Low Chicken Stock",
                "description": f"{chicken_days:.1f} days of chicken remaining. Schedule urgent delivery.",
                "outlet_id": outlet.outlet_id,
                "chicken_days": chicken_days
            })
        
        return alerts
    
    def check_all_outlets(self, outlets: List[Outlet], session: Session) -> List[dict]:
        """Check all outlets"""
        all_alerts = []
        for outlet in outlets:
            alerts = self.check_outlet(outlet, session)
            all_alerts.extend(alerts)
        return all_alerts


class AlertGenerator:
    """Converts detected issues into Risk records in database"""
    
    def create_risk_from_alert(self, alert: dict, session: Session) -> Risk:
        """Create a Risk record from alert data"""
        
        # Generate unique ID
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        risk_id = f"RISK-AUTO-{timestamp}"
        
        # Determine category
        if "supplier" in alert.get("type", ""):
            category = RiskCategory.SUPPLIER
        elif "inventory" in alert.get("type", ""):
            category = RiskCategory.DEMAND
        else:
            category = RiskCategory.EXTERNAL
        
        # Calculate impact
        impact_data = {
            "detected_at": datetime.now().isoformat(),
            "auto_generated": True
        }
        
        if "outlet_id" in alert:
            impact_data["affected_outlets"] = [alert["outlet_id"]]
            impact_data["estimated_revenue_at_risk"] = 500000  # PKR 5 Lakh per day
        
        if "supplier_id" in alert:
            impact_data["affected_supplier"] = alert["supplier_id"]
        
        # Create Risk
        risk = Risk(
            risk_id=risk_id,
            title=alert["title"],
            category=category,
            severity=alert["severity"],
            risk_score=75.0 if alert["severity"] == RiskSeverity.CRITICAL else 55.0,
            description=alert["description"],
            status=RiskStatus.ACTIVE,
            detection={
                "detected_at": datetime.now().isoformat(),
                "detected_by": "automated_monitor",
                "confidence": 0.95
            },
            impact=impact_data,
            recommendations=[
                {"priority": 1, "action": "Immediate review required", "effort": "low"},
                {"priority": 2, "action": "Contact operations team", "effort": "medium"}
            ]
        )
        
        session.add(risk)
        session.commit()
        session.refresh(risk)
        
        return risk
    
    def generate_alerts(self, detected_issues: List[dict], session: Session) -> List[Risk]:
        """Convert all detected issues to Risk records"""
        created_risks = []
        
        for issue in detected_issues:
            risk = self.create_risk_from_alert(issue, session)
            created_risks.append(risk)
            print(f"✅ Created alert: {risk.risk_id} - {risk.title}")
        
        return created_risks
