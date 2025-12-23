'use client'
import { useState, useEffect } from 'react'
import { api } from '@/lib/api'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Badge } from '@/components/ui/badge'
import { Supplier } from '@/lib/types'

export function SuppliersTable() {
    const [suppliers, setSuppliers] = useState<Supplier[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        api.suppliers.getAll()
            .then(data => setSuppliers(data))
            .catch(err => {
                console.error("Failed to load suppliers", err)
                setSuppliers([])
            })
            .finally(() => setLoading(false))
    }, [])

    if (loading) return <div className="space-y-2">
        {[1, 2, 3].map(i => <div key={i} className="h-12 bg-muted rounded animate-pulse" />)}
    </div>

    if (suppliers.length === 0) return <div className="p-4 text-center text-muted-foreground">No suppliers found</div>

    return (
        <Table>
            <TableHeader>
                <TableRow>
                    <TableHead>Name</TableHead>
                    <TableHead>Type</TableHead>
                    <TableHead>Tier</TableHead>
                    <TableHead>Location</TableHead>
                    <TableHead>Risk Score</TableHead>
                    <TableHead>Status</TableHead>
                </TableRow>
            </TableHeader>
            <TableBody>
                {suppliers.map(s => (
                    <TableRow key={s.supplier_id} className="cursor-pointer hover:bg-muted/50">
                        <TableCell className="font-medium">{s.name}</TableCell>
                        <TableCell className="capitalize">{s.type?.replace('_', ' ')}</TableCell>
                        <TableCell className="capitalize">{s.category?.replace('_', ' ')}</TableCell>
                        <TableCell>{s.location?.city || '-'}</TableCell>
                        <TableCell>
                            <span className={`font-bold ${s.risk_score > 70 ? 'text-red-500' : s.risk_score > 40 ? 'text-amber-500' : 'text-green-500'}`}>
                                {s.risk_score}
                            </span>
                        </TableCell>
                        <TableCell>
                            <Badge variant={s.current_status === 'critical' ? 'destructive' : s.current_status === 'warning' ? 'secondary' : 'default'}>
                                {s.current_status}
                            </Badge>
                        </TableCell>
                    </TableRow>
                ))}
            </TableBody>
        </Table>
    )
}
