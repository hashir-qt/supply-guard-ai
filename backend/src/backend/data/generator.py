from datetime import date, datetime, timedelta
from backend.models.schemas import (
    Supplier, Outlet, DeliveryRoute, Risk, CalendarEvent, HistoricalIncident,
    SupplierType, SupplierTier, OutletType, DeliveryStatus, RiskSeverity, RiskCategory, RiskStatus, EventType
)

# Demo Context: Current Date is roughly Jan 15, 2026

def generate_suppliers() -> list[Supplier]:
    return [
        Supplier(
            supplier_id="SUP-001", name="K&N's Foods", type=SupplierType.CHICKEN_PROCESSOR, category=SupplierTier.TIER_1,
            location={"city": "Karachi", "area": "Korangi Industrial"},
            metrics={"reliability": 94, "quality": 97, "lead_time": 24},
            risk_factors={"single_source": False, "concentration": 0.35},
            active_alerts=["Avian flu nearby farms"]
        ),
        Supplier(
            supplier_id="SUP-002", name="PK Meat Company", type=SupplierType.CHICKEN_PROCESSOR, category=SupplierTier.TIER_1,
            location={"city": "Lahore"},
            metrics={"reliability": 96, "quality": 98}, risk_factors={"concentration": 0.25}
        ),
        Supplier(
            supplier_id="SUP-003", name="Zenith Poultry", type=SupplierType.CHICKEN_PROCESSOR, category=SupplierTier.TIER_1,
            location={"city": "Rawalpindi"},
            metrics={"reliability": 92, "quality": 95}, risk_factors={"concentration": 0.15}
        ),
        Supplier(
            supplier_id="SUP-004", name="Malik Farms", type=SupplierType.POULTRY_FARM, category=SupplierTier.TIER_2,
            location={"city": "Lahore"},
            metrics={"reliability": 85, "quality": 90}, 
            risk_factors={"geographic_risk": "high", "disease_risk": "critical"},
            active_alerts=["Avian Flu Confirmed"]
        ),
        Supplier(
            supplier_id="SUP-005", name="Karachi Poultry Farms", type=SupplierType.POULTRY_FARM, category=SupplierTier.TIER_2,
            location={"city": "Karachi"},
            metrics={"reliability": 95, "quality": 96}
        ),
        Supplier(
            supplier_id="SUP-006", name="Punjab Agro Farms", type=SupplierType.POULTRY_FARM, category=SupplierTier.TIER_2,
            location={"city": "Faisalabad"}, metrics={"reliability": 88}
        ),
        Supplier(
            supplier_id="SUP-007", name="Sabzi Mandi Direct", type=SupplierType.PRODUCE, category=SupplierTier.TIER_1,
            location={"city": "Multi-city"}, metrics={"reliability": 90}
        ),
        Supplier(
            supplier_id="SUP-008", name="Dawn Bread", type=SupplierType.BAKERY, category=SupplierTier.TIER_1,
            location={"city": "Multi-city"}, metrics={"reliability": 98}
        ),
        Supplier(
            supplier_id="SUP-009", name="Gourmet Bakery", type=SupplierType.BAKERY, category=SupplierTier.TIER_1,
            location={"city": "Lahore"}, metrics={"reliability": 94}
        ),
        Supplier(
            supplier_id="SUP-010", name="National Foods", type=SupplierType.SPICES, category=SupplierTier.TIER_1,
            location={"city": "Karachi"}, metrics={"reliability": 99}
        ),
        Supplier(
            supplier_id="SUP-011", name="Packages Limited", type=SupplierType.PACKAGING, category=SupplierTier.TIER_1,
            location={"city": "Lahore"}, metrics={"reliability": 91}
        ),
        Supplier(
            supplier_id="SUP-012", name="Tri-Pack Films", type=SupplierType.PACKAGING, category=SupplierTier.TIER_1,
            location={"city": "Karachi"}, metrics={"reliability": 95}
        ),
        Supplier(
            supplier_id="SUP-013", name="Nestle Pakistan", type=SupplierType.DAIRY, category=SupplierTier.TIER_1,
            location={"city": "Lahore"}, metrics={"reliability": 99}
        ),
        Supplier(
            supplier_id="SUP-014",name="PSO Fuel", type=SupplierType.FUEL, category=SupplierTier.TIER_1,
            location={"city": "Multi-city"}, metrics={"reliability": 99}
        ),
        Supplier(
            supplier_id="SUP-015", name="Cold Chain Logistics", type=SupplierType.LOGISTICS_3PL, category=SupplierTier.TIER_1,
            location={"city": "Karachi"}, metrics={"reliability": 93}
        )
    ]

def generate_outlets() -> list[Outlet]:
    outlets = []
    
    # Karachi (12)
    khi_data = [
        ("KHI-001", "KFC Clifton", 72.0, 1.8), # Critical
        ("KHI-002", "KFC DHA Phase 5", 35.0, 4.2),
        ("KHI-003", "KFC Gulshan-e-Iqbal", 42.0, 3.5),
        ("KHI-004", "KFC Saddar", 28.0, 5.1),
        ("KHI-005", "KFC North Nazimabad", 55.0, 2.8),
        ("KHI-006", "KFC Tariq Road", 38.0, 3.9),
        ("KHI-007", "KFC Dolmen Mall Clifton", 25.0, 4.8),
        ("KHI-008", "KFC Lucky One Mall", 22.0, 5.2),
        ("KHI-009", "KFC Port Grand", 45.0, 3.2),
        ("KHI-010", "KFC Bahadurabad", 32.0, 4.5),
        ("KHI-011", "KFC Defence Phase 2", 28.0, 4.7),
        ("KHI-012", "KFC Korangi", 48.0, 2.5),
    ]
    for oid, name, score, days in khi_data:
        outlets.append(Outlet(
            outlet_id=oid, name=name, city="Karachi", zone="karachi", type=OutletType.STANDALONE,
            sales_trend="+5%",
            inventory={"chicken_days_remaining": days, "frozen_chicken_kg": int(days * 25)},
            operating_hours={"open": "11:00", "close": "01:00"}
        ))

    # Lahore (10)
    lhr_data = [
        ("LHR-001", "KFC Gulberg", 68.0, 2.1),
        ("LHR-002", "KFC DHA Lahore", 62.0, 2.4),
        ("LHR-003", "KFC Mall Road", 58.0, 2.8),
        ("LHR-004", "KFC Packages Mall", 52.0, 3.2),
        ("LHR-005", "KFC Johar Town", 55.0, 3.0),
        ("LHR-006", "KFC Model Town", 48.0, 3.5),
        ("LHR-007", "KFC Fortress Stadium", 45.0, 3.8),
        ("LHR-008", "KFC Emporium Mall", 42.0, 4.1),
        ("LHR-009", "KFC Bahria Town Lahore", 38.0, 4.5),
        ("LHR-010", "KFC Township", 35.0, 4.2),
    ]
    for oid, name, score, days in lhr_data:
        outlets.append(Outlet(
            outlet_id=oid, name=name, city="Lahore", zone="lahore", type=OutletType.STANDALONE,
            sales_trend="+2%",
            inventory={"chicken_days_remaining": days, "frozen_chicken_kg": int(days * 22)}
        ))

    # Islamabad (5) + Others (3)
    others = [
        ("ISL-001", "KFC F-7 Markaz", "Islamabad", 32.0, 4.8),
        ("ISL-002", "KFC Blue Area", "Islamabad", 28.0, 5.2),
        ("ISL-003", "KFC Centaurus Mall", "Islamabad", 25.0, 5.5),
        ("ISL-004", "KFC Bahria Town Islamabad", "Islamabad", 35.0, 4.5),
        ("ISL-005", "KFC F-10 Markaz", "Islamabad", 30.0, 5.0),
        ("MUL-001", "KFC Multan Cantt", "Multan", 42.0, 3.8),
        ("FSD-001", "KFC Faisalabad D-Ground", "Faisalabad", 45.0, 3.5),
        ("PSH-001", "KFC Peshawar Saddar", "Peshawar", 52.0, 3.2),
    ]
    for oid, name, city, score, days in others:
        outlets.append(Outlet(
            outlet_id=oid, name=name, city=city, zone=city.lower(), type=OutletType.STANDALONE,
            sales_trend="stable",
            inventory={"chicken_days_remaining": days}
        ))
        
    return outlets

def generate_routes() -> list[DeliveryRoute]:
    routes = []
    # Just creating a few representative ones
    route_data = [
        ("RT-KHI-01", "Karachi South", "Korangi CDC", ["KHI-001", "KHI-002"], DeliveryStatus.ON_ROUTE),
        ("RT-KHI-02", "Karachi Central", "Korangi CDC", ["KHI-003", "KHI-005"], DeliveryStatus.COMPLETED),
        ("RT-LHR-01", "Lahore Central", "Lahore CDC", ["LHR-001", "LHR-003"], DeliveryStatus.DELAYED),
        ("RT-ISL-01", "Islamabad Central", "Islamabad CDC", ["ISL-001", "ISL-002"], DeliveryStatus.COMPLETED),
    ]
    # Fill up to 18 roughly
    for i in range(1, 19):
         # basic generation for the rest
         if i <= 4: continue
         routes.append(DeliveryRoute(
             route_id=f"RT-GEN-{i:02d}", name=f"Route {i}", origin={"name": "CDC"}, 
             current_status=DeliveryStatus.SCHEDULED, schedule={"dep": "04:00"}
         ))

    for rid, name, origin, served, status in route_data:
        routes.append(DeliveryRoute(
            route_id=rid, name=name, origin={"name": origin}, outlets_served=served,
            current_status=status, schedule={"departure": "04:00"},
            metrics={"distance_km": 45, "on_time_rate": 89}
        ))
    return routes

def generate_risks() -> list[Risk]:
    risks = [
        Risk(
            risk_id="RISK-2026-001", title="Avian Flu Outbreak - Lahore Region", category=RiskCategory.SUPPLIER,
            severity=RiskSeverity.CRITICAL, risk_score=85.0, status=RiskStatus.ACTIVE,
            description="Avian influenza detected at 2 poultry farms in Lahore region.",
            detection={"date": "2026-01-12", "confidence": 0.89},
            impact={"revenue_at_risk_pkr": 23000000, "outlets": ["LHR-001", "LHR-002"]},
            recommendations=[
                {"action": "Activate Karachi backup supplier", "priority": 1},
                {"action": "Reduce menu to core items", "priority": 2}
            ]
        ),
        Risk(
            risk_id="RISK-2026-002", title="PSL Final Demand Surge", category=RiskCategory.DEMAND,
            severity=RiskSeverity.CRITICAL, risk_score=78.0, status=RiskStatus.ACTIVE,
            description="PSL Final in 5 days requiring 300% demand surge preparation.",
            impact={"forecast_surge": "300%", "stockout_prob": "high"}
        ),
        Risk(
            risk_id="RISK-2026-003", title="Karachi Port Congestion", category=RiskCategory.LOGISTICS,
            severity=RiskSeverity.HIGH, risk_score=65.0, status=RiskStatus.MONITORING,
            description="Port congestion building up, delaying imported packaging."
        ),
        Risk(
            risk_id="RISK-2026-004", title="K&N's Capacity Strain", category=RiskCategory.SUPPLIER,
            severity=RiskSeverity.HIGH, risk_score=62.0, status=RiskStatus.ACTIVE,
            description="Supplier operating at 98% capacity."
        )
    ]
    # Add dummy risks to reach 12
    for i in range(5, 13):
        risks.append(Risk(
            risk_id=f"RISK-2026-{i:03d}", title=f"Minor Risk {i}", category=RiskCategory.EXTERNAL,
            severity=RiskSeverity.LOW, risk_score=20.0 + i, status=RiskStatus.MONITORING,
            description=f"Automated risk alert {i}"
        ))
    return risks

def generate_events() -> list[CalendarEvent]:
    return [
        CalendarEvent(
            event_id="EVT-2026-PSL", name="PSL 2026 Final", type=EventType.SPORTS,
            start_date=date(2026, 1, 20), end_date=date(2026, 1, 20),
            impact_on_demand={"pattern": "surge", "multiplier": 3.0}, preparation_lead_days=7, risk_level="high"
        ),
        CalendarEvent(
            event_id="EVT-2026-RAM", name="Ramadan 2026", type=EventType.RELIGIOUS,
            start_date=date(2026, 3, 1), end_date=date(2026, 3, 30), # Approx dates
            impact_on_demand={"pattern": "shift"}, preparation_lead_days=14, risk_level="medium"
        ),
        CalendarEvent(
            event_id="EVT-2026-EID1", name="Eid-ul-Fitr", type=EventType.RELIGIOUS,
            start_date=date(2026, 3, 31), end_date=date(2026, 4, 2),
            impact_on_demand={"pattern": "surge", "multiplier": 2.5}, preparation_lead_days=10, risk_level="high"
        ),
        CalendarEvent(
             event_id="EVT-2026-PAK", name="Pakistan Day", type=EventType.HOLIDAY,
             start_date=date(2026, 3, 23), end_date=date(2026, 3, 23),
             impact_on_demand={"multiplier": 1.5}, preparation_lead_days=3, risk_level="low"
        )
    ]

def generate_history() -> list[HistoricalIncident]:
    return [
        HistoricalIncident(
            incident_id="INC-2025-001", date=date(2025, 7, 15), type="weather_flooding",
            description="Urban flooding in Karachi due to heavy monsoon rains", duration_days=3,
            impact={"revenue_loss": 8500000}, lessons_learned="Pre-position inventory"
        ),
        HistoricalIncident(
            incident_id="INC-2025-002", date=date(2025, 11, 5), type="supplier_outage",
            description="Avian flu outbreak in Lahore", duration_days=14,
            impact={"revenue_loss": 12300000}, lessons_learned="Diversify suppliers"
        )
    ]
