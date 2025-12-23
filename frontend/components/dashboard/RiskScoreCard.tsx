'use client'
import { TrendingUp, TrendingDown, Minus } from 'lucide-react'
import { cn } from '@/lib/utils'

interface Props {
    title: string
    score: number
    trend: 'improving' | 'stable' | 'degrading'
    trendValue: number
    icon: React.ReactNode
}

export function RiskScoreCard({ title, score, trend, trendValue, icon }: Props) {
    const getColor = (score: number) => {
        if (score >= 70) return { text: 'text-red-500', ring: 'stroke-red-500', bg: 'bg-red-500/10' }
        if (score >= 50) return { text: 'text-orange-500', ring: 'stroke-orange-500', bg: 'bg-orange-500/10' }
        if (score >= 30) return { text: 'text-yellow-500', ring: 'stroke-yellow-500', bg: 'bg-yellow-500/10' }
        return { text: 'text-green-500', ring: 'stroke-green-500', bg: 'bg-green-500/10' }
    }

    const getStatus = (score: number) => {
        if (score >= 70) return 'Critical'
        if (score >= 50) return 'High'
        if (score >= 30) return 'Medium'
        return 'Low'
    }

    const colors = getColor(score)
    const circumference = 2 * Math.PI * 36
    const offset = circumference - (score / 100) * circumference

    return (
        <div className="bg-card rounded-xl p-5 border border-border hover:border-ring/50 transition-all shadow-sm text-card-foreground">
            <div className="flex items-center justify-between mb-4">
                <div className={cn("p-2 rounded-lg", colors.bg)}>
                    {icon}
                </div>
                <span className={cn("text-xs font-medium px-2 py-1 rounded-full", colors.bg, colors.text)}>
                    {getStatus(score)}
                </span>
            </div>

            <div className="flex items-center justify-between">
                <div className="relative w-20 h-20">
                    <svg className="w-20 h-20 transform -rotate-90">
                        <circle cx="40" cy="40" r="36" className="stroke-muted" strokeWidth="6" fill="none" />
                        <circle
                            cx="40" cy="40" r="36"
                            className={cn(colors.ring, "transition-all duration-700")}
                            strokeWidth="6"
                            fill="none"
                            strokeLinecap="round"
                            strokeDasharray={circumference}
                            strokeDashoffset={offset}
                        />
                    </svg>
                    <div className="absolute inset-0 flex items-center justify-center">
                        <span className={cn("text-2xl font-bold", colors.text)}>{score}</span>
                    </div>
                </div>

                <div>
                    <h3 className="font-semibold mb-2">{title}</h3>
                    <div className="flex items-center gap-1 text-sm">
                        {trend === 'improving' && <TrendingDown className="w-4 h-4 text-green-400" />}
                        {trend === 'degrading' && <TrendingUp className="w-4 h-4 text-red-400" />}
                        {trend === 'stable' && <Minus className="w-4 h-4 text-gray-400" />}
                        <span className={trend === 'improving' ? 'text-green-400' : trend === 'degrading' ? 'text-red-400' : 'text-gray-400'}>
                            {trendValue > 0 ? '+' : ''}{trendValue}
                        </span>
                    </div>
                </div>
            </div>
        </div>
    )
}
