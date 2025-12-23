'use client'
import { useState, useEffect } from 'react'
import { api } from '@/lib/api'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Badge } from '@/components/ui/badge'
import { Outlet } from '@/lib/types'

export function OutletsTable() {
    const [outlets, setOutlets] = useState<Outlet[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        api.outlets.getAll()
            .then(data => setOutlets(data))
            .catch(err => {
                console.error("Failed to load outlets", err)
                setOutlets([])
            })
            .finally(() => setLoading(false))
    }, [])

    if (loading) return <div className="space-y-2">
        {[1, 2, 3].map(i => <div key={i} className="h-12 bg-muted rounded animate-pulse" />)}
    </div>

    if (outlets.length === 0) return <div className="p-4 text-center text-muted-foreground">No outlets found</div>

    return (
        <Table>
            <TableHeader>
                <TableRow>
                    <TableHead>Name</TableHead>
                    <TableHead>City</TableHead>
                    <TableHead>Type</TableHead>
                    <TableHead>Inventory Status</TableHead>
                    <TableHead>Risk Score</TableHead>
                </TableRow>
            </TableHeader>
            <TableBody>
                {outlets.map(o => (
                    <TableRow key={o.outlet_id} className="cursor-pointer hover:bg-muted/50">
                        <TableCell className="font-medium">{o.name}</TableCell>
                        <TableCell>{o.city}</TableCell>
                        <TableCell className="capitalize">{o.type}</TableCell>
                        <TableCell>
                            {o.inventory ? (
                                <div className="grid gap-1">
                                    <span className="text-xs">Chicken: {Math.round(o.inventory.frozen_chicken_kg || 0)}kg</span>
                                    <span className={`text-xs font-bold ${o.inventory.chicken_days_remaining < 2 ? 'text-red-500' : 'text-green-500'}`}>
                                        {o.inventory.chicken_days_remaining?.toFixed(1)} days left
                                    </span>
                                </div>
                            ) : '-'}
                        </TableCell>
                        <TableCell>
                            <span className={`font-bold ${o.current_risk_score > 70 ? 'text-red-500' : o.current_risk_score > 40 ? 'text-amber-500' : 'text-green-500'}`}>
                                {o.current_risk_score}
                            </span>
                        </TableCell>
                    </TableRow>
                ))}
            </TableBody>
        </Table>
    )
}
