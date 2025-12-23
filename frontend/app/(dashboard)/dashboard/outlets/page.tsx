import { OutletsTable } from '@/components/outlets/OutletsTable'

export default function OutletsPage() {
    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-2xl font-bold">Outlet Management</h1>
                <p className="text-muted-foreground">Monitor outlet inventory and risk status</p>
            </div>

            <div className="bg-card rounded-xl border border-border overflow-hidden">
                <OutletsTable />
            </div>
        </div>
    )
}
