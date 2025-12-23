'use client'
import { useOverview } from '@/hooks/useOverview'
import { RiskScoreCard } from './RiskScoreCard'
import { Factory, Truck, TrendingUp, Cloud } from 'lucide-react'

export function RiskScoreGrid() {
    const { data, loading } = useOverview()

    if (loading) return <div className="grid grid-cols-4 gap-4">
        {[1, 2, 3, 4].map(i => <div key={i} className="h-40 bg-gray-900 rounded-xl animate-pulse" />)}
    </div>

    if (!data) return null

    const categories = [
        { key: 'supplier', title: 'Supplier Risk', icon: <Factory className="w-5 h-5" /> },
        { key: 'logistics', title: 'Logistics Risk', icon: <Truck className="w-5 h-5" /> },
        { key: 'demand', title: 'Demand Risk', icon: <TrendingUp className="w-5 h-5" /> },
        { key: 'external', title: 'External Risk', icon: <Cloud className="w-5 h-5" /> },
    ]

    // Calculate category scores from available data
    const categoryScores = {
        supplier: data.overall_health_score * 0.9, // Mock based on overall health
        logistics: data.overall_health_score * 1.1,
        demand: data.overall_health_score * 0.95,
        external: data.overall_health_score * 1.05,
    }

    const categoryTrends: Record<string, 'improving' | 'stable' | 'degrading'> = {
        supplier: data.active_risks > 5 ? 'degrading' : 'stable',
        logistics: 'stable',
        demand: 'improving',
        external: data.critical_alerts > 0 ? 'degrading' : 'stable',
    }

    return (
        <div className="grid grid-cols-4 gap-4">
            {categories.map(cat => (
                <RiskScoreCard
                    key={cat.key}
                    title={cat.title}
                    score={categoryScores[cat.key as keyof typeof categoryScores]}
                    trend={categoryTrends[cat.key as keyof typeof categoryTrends]}
                    trendValue={Math.floor(Math.random() * 10) - 5} // Mock trend value
                    icon={cat.icon}
                />
            ))}
        </div>
    )
}
