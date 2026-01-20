'use client'
import { useState } from 'react'
import { AlertsTable } from '@/components/risks/AlertsTable'
import { RiskDetailModal } from '@/components/risks/RiskDetailModal'
import { Risk } from '@/lib/types'

export default function RisksPage() {
    const [selectedRisk, setSelectedRisk] = useState<Risk | null>(null)
    const [modalOpen, setModalOpen] = useState(false)

    const handleViewDetails = (risk: Risk) => {
        setSelectedRisk(risk)
        setModalOpen(true)
    }

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-2xl font-bold">Risk Management</h1>
                <p className="text-muted-foreground">Monitor and mitigate supply chain threats</p>
            </div>

            <div className="bg-card rounded-xl border border-border overflow-hidden">
                <div className="p-6 border-b border-border">
                    <h2 className="font-semibold text-lg">All Risks</h2>
                </div>
                <AlertsTable onViewDetails={handleViewDetails} />
            </div>

            <RiskDetailModal
                risk={selectedRisk}
                open={modalOpen}
                onOpenChange={setModalOpen}
            />
        </div>
    )
}
