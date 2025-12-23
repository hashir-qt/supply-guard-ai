'use client'
import { useOverview } from '@/hooks/useOverview'
import { Store, AlertTriangle, Truck, Activity } from 'lucide-react'

export function OverviewMetrics() {
    const { data, loading } = useOverview()

    if (loading) return <div className="grid grid-cols-4 gap-4">
        {[1, 2, 3, 4].map(i => <div key={i} className="h-24 bg-card rounded-xl animate-pulse" />)}
    </div>

    if (!data) return null

    const metrics = [
        {
            label: 'Total Outlets',
            value: data.total_outlets,
            icon: Store,
            color: 'text-blue-400',
            bg: 'bg-blue-500/10'
        },
        {
            label: 'At-Risk Outlets',
            value: data.outlets_at_risk,
            icon: AlertTriangle,
            color: 'text-red-400',
            bg: 'bg-red-500/10'
        },
        {
            label: 'Active Alerts',
            value: data.active_risks,
            icon: Activity,
            color: 'text-orange-400',
            bg: 'bg-orange-500/10'
        },
        {
            label: 'Deliveries Today',
            value: data.active_deliveries,
            icon: Truck,
            color: 'text-green-400',
            bg: 'bg-green-500/10'
        }
    ]

    return (
        <div className="grid grid-cols-4 gap-4">
            {metrics.map((metric) => {
                const Icon = metric.icon
                return (
                    <div key={metric.label} className="bg-card rounded-xl p-5 border border-border text-card-foreground shadow-sm">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-muted-foreground mb-1">{metric.label}</p>
                                <p className="text-3xl font-bold">{metric.value}</p>
                            </div>
                            <div className={`p-3 rounded-lg ${metric.bg}`}>
                                <Icon className={`w-6 h-6 ${metric.color}`} />
                            </div>
                        </div>
                    </div>
                )
            })}
        </div>
    )
}
