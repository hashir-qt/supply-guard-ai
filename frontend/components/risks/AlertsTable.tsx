'use client'
import { useState, useEffect } from 'react'
import { api } from '@/lib/api'
import { SeverityBadge } from './SeverityBadge'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Badge } from '@/components/ui/badge'
import { Risk } from '@/lib/types'

export function AlertsTable({ limit }: { limit?: number }) {
    const [alerts, setAlerts] = useState<Risk[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        api.risks.getAll()
            .then(data => setAlerts(limit ? data.slice(0, limit) : data))
            .catch(err => {
                console.error("Failed to load alerts", err)
                setAlerts([])
            })
            .finally(() => setLoading(false))
    }, [limit])

    if (loading) return <div className="space-y-2">
        {[1, 2, 3].map(i => <div key={i} className="h-12 bg-muted rounded animate-pulse" />)}
    </div>

    if (alerts.length === 0) {
        return <div className="p-4 text-center text-muted-foreground">No active risks found (Backend might be starting up)</div>
    }

    return (
        <Table>
            <TableHeader>
                <TableRow>
                    <TableHead>Severity</TableHead>
                    <TableHead>Risk</TableHead>
                    <TableHead>Category</TableHead>
                    <TableHead>Impact</TableHead>
                    <TableHead>Status</TableHead>
                </TableRow>
            </TableHeader>
            <TableBody>
                {alerts.map(alert => (
                    <TableRow key={alert.risk_id} className="cursor-pointer hover:bg-muted/50">
                        <TableCell><SeverityBadge severity={alert.severity} /></TableCell>
                        <TableCell className="font-medium">
                            <div>{alert.title}</div>
                            <div className="text-xs text-muted-foreground">{alert.description}</div>
                        </TableCell>
                        <TableCell><Badge variant="outline">{alert.category}</Badge></TableCell>
                        <TableCell className="text-sm text-muted-foreground">
                            {alert.impact ? (
                                <div className="space-y-1">
                                    {alert.impact.affected_outlets && <div>Outlets: {alert.impact.affected_outlets}</div>}
                                    {alert.impact.revenue_at_risk && <div>Rev: {alert.impact.revenue_at_risk}</div>}
                                </div>
                            ) : '-'}
                        </TableCell>
                        <TableCell><Badge>{alert.status}</Badge></TableCell>
                    </TableRow>
                ))}
            </TableBody>
        </Table>
    )
}
