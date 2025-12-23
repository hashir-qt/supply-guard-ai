'use client'
import { useState } from 'react'
import { api } from '@/lib/api'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Slider } from '@/components/ui/slider'
import { Label } from '@/components/ui/label'
import { SimulationResult } from '@/lib/types'
import { Loader2, TrendingDown, DollarSign, Archive, AlertOctagon } from 'lucide-react'

export default function SimulationPage() {
    const [loading, setLoading] = useState(false)
    const [result, setResult] = useState<SimulationResult | null>(null)

    // Form State
    const [type, setType] = useState('supplier_failure')
    const [severity, setSeverity] = useState('high')
    const [duration, setDuration] = useState([7])

    const handleRun = async () => {
        setLoading(true)
        try {
            const data = await api.simulation.run({
                disruption_type: type,
                severity,
                duration_days: duration[0]
            })
            setResult(data)
        } catch (e) {
            console.error(e)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-2xl font-bold">Risk Simulator</h1>
                <p className="text-muted-foreground">Simulate potential supply chain disruptions and model their impact</p>
            </div>

            <div className="grid md:grid-cols-12 gap-6">
                {/* Controls */}
                <div className="md:col-span-4 space-y-6">
                    <Card>
                        <CardHeader>
                            <CardTitle>Simulation Parameters</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-6">
                            <div className="space-y-2">
                                <Label>Disruption Type</Label>
                                <Select value={type} onValueChange={setType}>
                                    <SelectTrigger>
                                        <SelectValue />
                                    </SelectTrigger>
                                    <SelectContent>
                                        <SelectItem value="supplier_failure">Major Supplier Failure</SelectItem>
                                        <SelectItem value="logistics_strike">Logistics Strike</SelectItem>
                                        <SelectItem value="demand_surge">Unexpected Demand Surge</SelectItem>
                                        <SelectItem value="port_closure">Port Closure</SelectItem>
                                    </SelectContent>
                                </Select>
                            </div>

                            <div className="space-y-2">
                                <Label>Severity Level</Label>
                                <Select value={severity} onValueChange={setSeverity}>
                                    <SelectTrigger>
                                        <SelectValue />
                                    </SelectTrigger>
                                    <SelectContent>
                                        <SelectItem value="low">Low (Partial Impact)</SelectItem>
                                        <SelectItem value="medium">Medium (Significant Delays)</SelectItem>
                                        <SelectItem value="high">High (Complete Stoppage)</SelectItem>
                                    </SelectContent>
                                </Select>
                            </div>

                            <div className="space-y-4">
                                <div className="flex justify-between">
                                    <Label>Duration (Days)</Label>
                                    <span className="text-sm font-medium">{duration[0]} days</span>
                                </div>
                                <Slider
                                    value={duration}
                                    onValueChange={setDuration}
                                    max={60}
                                    min={1}
                                    step={1}
                                />
                            </div>

                            <Button
                                onClick={handleRun}
                                className="w-full bg-blue-600 hover:bg-blue-700 text-white"
                                disabled={loading}
                            >
                                {loading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                                Run Simulation
                            </Button>
                        </CardContent>
                    </Card>
                </div>

                {/* Results */}
                <div className="md:col-span-8">
                    {result ? (
                        <div className="space-y-6">
                            {/* Summary Cards */}
                            <div className="grid sm:grid-cols-3 gap-4">
                                <Card>
                                    <CardContent className="pt-6">
                                        <div className="flex items-center gap-4">
                                            <div className="p-3 bg-red-100 text-red-600 rounded-full">
                                                <DollarSign className="w-6 h-6" />
                                            </div>
                                            <div>
                                                <p className="text-sm text-gray-500">Revenue at Risk</p>
                                                <p className="text-2xl font-bold">PKR {result.impact_summary.revenue_at_risk?.toLocaleString()}</p>
                                            </div>
                                        </div>
                                    </CardContent>
                                </Card>
                                <Card>
                                    <CardContent className="pt-6">
                                        <div className="flex items-center gap-4">
                                            <div className="p-3 bg-amber-100 text-amber-600 rounded-full">
                                                <Store className="w-6 h-6" />
                                            </div>
                                            <div>
                                                <p className="text-sm text-gray-500">Outlets Affected</p>
                                                <p className="text-2xl font-bold">{result.impact_summary.outlets_affected}</p>
                                            </div>
                                        </div>
                                    </CardContent>
                                </Card>
                                <Card>
                                    <CardContent className="pt-6">
                                        <div className="flex items-center gap-4">
                                            <div className="p-3 bg-blue-100 text-blue-600 rounded-full">
                                                <Archive className="w-6 h-6" />
                                            </div>
                                            <div>
                                                <p className="text-sm text-gray-500">Inventory Shortfall</p>
                                                <p className="text-2xl font-bold">{result.impact_summary.inventory_shortfall_kg?.toLocaleString()} kg</p>
                                            </div>
                                        </div>
                                    </CardContent>
                                </Card>
                            </div>

                            {/* Timeline */}
                            <Card>
                                <CardHeader>
                                    <CardTitle>Cascade Effect Timeline</CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <div className="relative border-l-2 border-slate-200 ml-4 space-y-8 pb-4">
                                        {result.timeline.map((event: any, idx) => (
                                            <div key={idx} className="relative pl-8">
                                                <div className="absolute -left-2.5 top-0 w-5 h-5 bg-white border-2 border-blue-500 rounded-full"></div>
                                                <div>
                                                    <span className="text-sm font-semibold text-blue-600">Day {event.day}</span>
                                                    <p className="font-medium text-slate-900 mt-1">{event.event}</p>
                                                    <p className="text-sm text-slate-500">{event.impact}</p>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </CardContent>
                            </Card>

                            {/* Recommendations */}
                            <Card className="border-l-4 border-l-green-500">
                                <CardHeader>
                                    <CardTitle className="text-green-700">AI Recommendations</CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <ul className="space-y-3">
                                        {result.recommendations.map((rec, idx) => (
                                            <li key={idx} className="flex items-start gap-2">
                                                <span className="mt-1.5 w-1.5 h-1.5 bg-green-500 rounded-full shrink-0"></span>
                                                <span className="text-slate-700">{rec}</span>
                                            </li>
                                        ))}
                                    </ul>
                                </CardContent>
                            </Card>

                        </div>
                    ) : (
                        <div className="h-full min-h-[400px] flex flex-col items-center justify-center text-slate-400 border-2 border-dashed border-slate-200 rounded-xl bg-slate-50/50">
                            <AlertOctagon className="w-16 h-16 mb-4 opacity-20" />
                            <p className="text-lg font-medium">Ready to Simulate</p>
                            <p className="text-sm">Adjust parameters and click "Run Simulation" to see AI predictions.</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}

// Helper icon import (Store was missing in imports)
import { Store } from 'lucide-react'
