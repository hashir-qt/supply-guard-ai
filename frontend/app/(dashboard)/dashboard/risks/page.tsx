import { AlertsTable } from '@/components/risks/AlertsTable'

export default function RisksPage() {
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
                <AlertsTable />
            </div>
        </div>
    )
}
