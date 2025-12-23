from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime, date
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import JSON, Column

# --- Enums ---

class RiskSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class RiskCategory(str, Enum):
    SUPPLIER = "supplier"
    LOGISTICS = "logistics"
    DEMAND = "demand"
    EXTERNAL = "external"

class SupplierType(str, Enum):
    CHICKEN_PROCESSOR = "chicken_processor"
    POULTRY_FARM = "poultry_farm"
    PRODUCE = "fresh_produce"
    BAKERY = "bakery"
    PACKAGING = "packaging"
    DAIRY = "dairy"
    SPICES = "sauces_spices"
    FUEL = "fuel"
    LOGISTICS_3PL = "3pl_logistics"

class SupplierTier(str, Enum):
    TIER_1 = "tier_1"
    TIER_2 = "tier_2"
    TIER_3 = "tier_3"

class OutletType(str, Enum):
    STANDALONE = "standalone"
    MALL = "mall"
    DRIVE_THROUGH = "drive_through"
    EXPRESS = "express"

class ZoneName(str, Enum):
    KARACHI = "karachi"
    LAHORE = "lahore"
    ISLAMABAD = "islamabad"
    MULTAN = "multan"
    FAISALABAD = "faisalabad"
    PESHAWAR = "peshawar"
    OTHER = "other"

class DeliveryStatus(str, Enum):
    SCHEDULED = "scheduled"
    ON_ROUTE = "on_route"
    COMPLETED = "completed"
    DELAYED = "delayed"
    CANCELLED = "cancelled"

class RiskStatus(str, Enum):
    ACTIVE = "active"
    MITIGATED = "mitigated"
    RESOLVED = "resolved"
    MONITORING = "monitoring"

class EventType(str, Enum):
    RELIGIOUS = "religious"
    SPORTS = "sports"
    HOLIDAY = "holiday"
    WEATHER = "weather"
    POLITICAL = "political"

# --- Models ---

class Supplier(SQLModel, table=True):
    supplier_id: str = Field(primary_key=True)
    name: str
    type: SupplierType
    category: SupplierTier
    location: Dict = Field(default={}, sa_column=Column(JSON))  # {city, area}
    products_supplied: List[str] = Field(default=[], sa_column=Column(JSON))
    outlets_served: List[str] = Field(default=[], sa_column=Column(JSON))
    metrics: Dict = Field(default={}, sa_column=Column(JSON))  # {reliability_score, quality_score...}
    risk_factors: Dict = Field(default={}, sa_column=Column(JSON))
    active_alerts: List[str] = Field(default=[], sa_column=Column(JSON))
    contract_end_date: Optional[date] = None
    ai_analysis: Optional[Dict] = Field(default={}, sa_column=Column(JSON))

class Outlet(SQLModel, table=True):
    outlet_id: str = Field(primary_key=True)
    name: str
    city: str
    zone: str
    type: OutletType
    coordinates: Dict = Field(default={}, sa_column=Column(JSON)) # {lat, lng}
    operating_hours: Dict = Field(default={}, sa_column=Column(JSON))
    capacity: Dict = Field(default={}, sa_column=Column(JSON))
    inventory: Dict = Field(default={}, sa_column=Column(JSON)) # {frozen_chicken_kg, chicken_days_remaining...}
    equipment_status: Dict = Field(default={}, sa_column=Column(JSON))
    sales_trend: str
    last_delivery: Optional[datetime] = None
    next_delivery: Optional[datetime] = None

class DeliveryRoute(SQLModel, table=True):
    route_id: str = Field(primary_key=True)
    name: str
    origin: Dict = Field(default={}, sa_column=Column(JSON))
    outlets_served: List[str] = Field(default=[], sa_column=Column(JSON))
    schedule: Dict = Field(default={}, sa_column=Column(JSON))
    metrics: Dict = Field(default={}, sa_column=Column(JSON))
    current_status: DeliveryStatus
    vehicle: Dict = Field(default={}, sa_column=Column(JSON))
    risk_factors: Dict = Field(default={}, sa_column=Column(JSON))

class Risk(SQLModel, table=True):
    risk_id: str = Field(primary_key=True)
    title: str
    category: RiskCategory
    severity: RiskSeverity
    risk_score: float
    description: str
    detection: Dict = Field(default={}, sa_column=Column(JSON)) # {detected_at, detected_by}
    impact: Dict = Field(default={}, sa_column=Column(JSON)) # {affected_outlets, revenue_at_risk...}
    cascade_effects: List[Dict] = Field(default=[], sa_column=Column(JSON))
    recommendations: List[Dict] = Field(default=[], sa_column=Column(JSON))
    status: RiskStatus
    owner: Optional[str] = "Supply Chain Manager"
    last_updated: datetime = Field(default_factory=datetime.utcnow)

class CalendarEvent(SQLModel, table=True):
    event_id: str = Field(primary_key=True)
    name: str
    type: EventType
    start_date: date
    end_date: date
    impact_on_demand: Dict = Field(default={}, sa_column=Column(JSON))
    affected_zones: List[str] = Field(default=[], sa_column=Column(JSON))
    preparation_lead_days: int
    risk_level: str

class HistoricalIncident(SQLModel, table=True):
    incident_id: str = Field(primary_key=True)
    date: date
    type: str # keeping as string to allow flexibility matching Risk categories or others
    description: str
    duration_days: int
    impact: Dict = Field(default={}, sa_column=Column(JSON))
    response: Dict = Field(default={}, sa_column=Column(JSON))
    lessons_learned: str

# --- API/Dashboard Transfer Models (Not Tables) ---

class RiskScoreCard(SQLModel):
    title: str
    score: float
    trend: str # "up", "down"
    status: str # "critical", "warning"

class SupplyChainOverview(SQLModel):
    total_suppliers: int
    total_outlets: int
    active_risks: int
    overall_health_score: float
    critical_alerts: int

class SimulationRequest(SQLModel):
    disruption_type: str
    severity: str
    duration_days: int

class SimulationResult(SQLModel):
    scenario_id: str
    timeline: List[Dict] = []
    impact_summary: Dict = {}
    recommendations: List[str] = []

class ChatRequest(SQLModel):
    message: str
    context: Optional[Dict] = {}

class ChatResponse(SQLModel):
    message: str
    actions: Optional[List[Dict]] = []

class CascadeStage(SQLModel):
    stage: int
    description: str
    time_days: int
    impact: str = ""

class RiskRecommendation(SQLModel):
    priority: int
    action: str
    effort: str
    impact: str
    deadline: Optional[str] = None

class DemandForecast(SQLModel):
    outlet_id: str
    forecast_date: str # or date
    predicted_orders: int
    confidence_score: float
    influencing_factors: List[str] = []
