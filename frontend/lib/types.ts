// Mirror backend Pydantic models from backend/src/backend/models/schemas.py

export type RiskSeverity = 'low' | 'medium' | 'high' | 'critical'
export type RiskCategory = 'supplier' | 'logistics' | 'demand' | 'external'
export type TrendDirection = 'improving' | 'stable' | 'degrading'
export type SupplierType = 'chicken_processor' | 'poultry_farm' | 'fresh_produce' | 'bakery' | 'packaging' | 'dairy' | 'sauces_spices' | 'fuel' | '3pl_logistics'
export type SupplierTier = 'tier_1' | 'tier_2' | 'tier_3'
export type OutletType = 'standalone' | 'mall' | 'drive_through' | 'express'
export type DeliveryStatus = 'scheduled' | 'on_route' | 'completed' | 'delayed' | 'cancelled'
export type RiskStatus = 'active' | 'mitigated' | 'resolved' | 'monitoring'

export interface SupplyChainOverview {
    total_suppliers: number
    total_outlets: number
    active_risks: number
    outlets_at_risk: number
    active_deliveries: number
    overall_health_score: number
    critical_alerts: number
}

// Corresponds to 'Risk' in schemas.py
export interface Risk {
    risk_id: string
    title: string
    category: RiskCategory
    severity: RiskSeverity
    risk_score: number
    description: string
    detection?: Record<string, any>
    impact?: Record<string, any>
    cascade_effects?: any[]
    recommendations?: any[]
    status: RiskStatus
    owner?: string
    last_updated: string
}

export interface Supplier {
    supplier_id: string
    name: string
    type: SupplierType
    category: SupplierTier
    location?: any
    products_supplied?: string[]
    outlets_served?: string[]
    metrics?: any
    risk_factors?: any
    current_status: string
    risk_score: number
    active_alerts?: string[]
    contract_end_date?: string
    ai_analysis?: any
}

export interface Outlet {
    outlet_id: string
    name: string
    city: string
    zone: string
    type: OutletType
    coordinates?: any
    operating_hours?: any
    capacity?: any
    inventory?: any
    equipment_status?: any
    current_risk_score: number
    sales_trend: string
    last_delivery?: string
    next_delivery?: string
}

export interface SimulationRequest {
    disruption_type: string
    severity: string
    duration_days: number
}

export interface SimulationResult {
    scenario_id: string
    timeline: any[]
    impact_summary: any
    recommendations: string[]
}

export interface ChatRequest {
    message: string
    context?: any
}

export interface ChatResponse {
    message: string
    actions?: any[]
}
