import { SuppliersTable } from '@/components/suppliers/SuppliersTable'

export default function SuppliersPage() {
    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-2xl font-bold">Supplier Network</h1>
                <p className="text-muted-foreground">Manage and monitor supplier health</p>
            </div>

            <div className="bg-card rounded-xl border border-border overflow-hidden">
                <SuppliersTable />
            </div>
        </div>
    )
}
