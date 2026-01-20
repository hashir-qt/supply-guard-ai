'use client'
import { Suspense, useState } from 'react'
import { OverviewMetrics } from '@/components/dashboard/OverviewMetrics'
import { RiskScoreGrid } from '@/components/dashboard/RiskScoreGrid'
import { AlertsTable } from '@/components/risks/AlertsTable'
import { RiskDetailModal } from '@/components/risks/RiskDetailModal'
import { AgentChat } from '@/components/chat/AgentChat'
import { Risk } from '@/lib/types'
import Link from 'next/link'

export default function DashboardPage() {
    const [selectedRisk, setSelectedRisk] = useState<Risk | null>(null)
    const [modalOpen, setModalOpen] = useState(false)

    const handleViewDetails = (risk: Risk) => {
        setSelectedRisk(risk)
        setModalOpen(true)
    }

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-2xl font-bold">Supply Chain Risk Dashboard</h1>
                <p className="text-muted-foreground">KFC Pakistan • Real-time Risk Intelligence</p>
            </div>

            <Suspense fallback={<div>Loading metrics...</div>}>
                <OverviewMetrics />
            </Suspense>

            <Suspense fallback={<div>Loading scores...</div>}>
                <RiskScoreGrid />
            </Suspense>

            <div className="grid grid-cols-12 gap-6 h-[600px]">
                <div className="col-span-8 space-y-6 h-full flex flex-col">
                    <div className="bg-card rounded-xl border border-border flex-1 overflow-hidden flex flex-col">
                        <div className="p-6 border-b border-border flex justify-between items-center">
                            <h2 className="font-semibold text-lg">Active Risk Alerts</h2>
                            <Link href="/dashboard/risks" className="text-sm text-blue-400 hover:text-blue-300">
                                View All
                            </Link>
                        </div>
                        <div className="flex-1 overflow-auto">
                            <Suspense fallback={<div>Loading alerts...</div>}>
                                <AlertsTable limit={10} onViewDetails={handleViewDetails} />
                            </Suspense>
                        </div>
                    </div>
                </div>

                <div className="col-span-4 h-full">
                    <AgentChat />
                </div>
            </div>

            <RiskDetailModal
                risk={selectedRisk}
                open={modalOpen}
                onOpenChange={setModalOpen}
            />
        </div>
    )
}
