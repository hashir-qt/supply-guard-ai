'use client'
import { useState, useEffect, useCallback } from 'react'
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogDescription,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { SeverityBadge } from './SeverityBadge'
import { Risk } from '@/lib/types'
import { api } from '@/lib/api'
import ReactMarkdown from 'react-markdown'

interface RiskDetailModalProps {
    risk: Risk | null
    open: boolean
    onOpenChange: (open: boolean) => void
}

export function RiskDetailModal({ risk, open, onOpenChange }: RiskDetailModalProps) {
    const [analysis, setAnalysis] = useState<string | null>(null)
    const [loading, setLoading] = useState(false)
    const [toolsUsed, setToolsUsed] = useState<string[]>([])
    const [analyzedRiskId, setAnalyzedRiskId] = useState<string | null>(null)

    const runAnalysis = useCallback(async (riskToAnalyze: Risk) => {
        setLoading(true)
        setAnalysis(null)

        try {
            const prompt = `Analyze this risk in detail and provide actionable recommendations:

Risk: ${riskToAnalyze.title}
Category: ${riskToAnalyze.category}
Severity: ${riskToAnalyze.severity}
Risk Score: ${riskToAnalyze.risk_score}
Description: ${riskToAnalyze.description}
${riskToAnalyze.impact ? `Impact: Affected outlets: ${riskToAnalyze.impact.affected_outlets || 'N/A'}, Revenue at risk: ${riskToAnalyze.impact.revenue_at_risk || 'N/A'}` : ''}

Please provide:
1. A detailed analysis of this risk
2. Potential cascade effects
3. Immediate actions to take
4. Long-term mitigation strategies`

            const response = await api.agent.chat(prompt)
            setAnalysis(response.response)
            setToolsUsed(response.tools_used || [])
            setAnalyzedRiskId(riskToAnalyze.risk_id)
        } catch {
            setAnalysis('Failed to analyze risk. Please try again.')
        } finally {
            setLoading(false)
        }
    }, [])

    useEffect(() => {
        if (open && risk && analyzedRiskId !== risk.risk_id) {
            runAnalysis(risk)
        }
    }, [open, risk, analyzedRiskId, runAnalysis])

    useEffect(() => {
        if (!open) {
            setAnalysis(null)
            setToolsUsed([])
            setAnalyzedRiskId(null)
        }
    }, [open])

    if (!risk) return null

    return (
        <Dialog open={open} onOpenChange={onOpenChange}>
            <DialogContent className="max-w-3xl max-h-[85vh] overflow-hidden flex flex-col">
                <DialogHeader>
                    <div className="flex items-center gap-3">
                        <SeverityBadge severity={risk.severity} />
                        <DialogTitle className="text-xl">{risk.title}</DialogTitle>
                    </div>
                    <DialogDescription>{risk.description}</DialogDescription>
                </DialogHeader>

                <div className="grid grid-cols-2 gap-4 py-4 border-y border-border">
                    <div className="space-y-2">
                        <div className="text-sm text-muted-foreground">Category</div>
                        <Badge variant="outline" className="capitalize">{risk.category}</Badge>
                    </div>
                    <div className="space-y-2">
                        <div className="text-sm text-muted-foreground">Status</div>
                        <Badge className="capitalize">{risk.status}</Badge>
                    </div>
                    <div className="space-y-2">
                        <div className="text-sm text-muted-foreground">Risk Score</div>
                        <div className="text-2xl font-bold text-red-500">{risk.risk_score.toFixed(0)}</div>
                    </div>
                    {risk.impact && (
                        <div className="space-y-2">
                            <div className="text-sm text-muted-foreground">Impact</div>
                            <div className="text-sm">
                                {risk.impact.affected_outlets && <div>Outlets: {risk.impact.affected_outlets}</div>}
                                {risk.impact.revenue_at_risk && <div>Revenue: {risk.impact.revenue_at_risk}</div>}
                            </div>
                        </div>
                    )}
                </div>

                <div className="flex-1 overflow-auto">
                    <div className="flex items-center justify-between mb-3">
                        <h3 className="font-semibold flex items-center gap-2">
                            <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                            AI Analysis
                        </h3>
                        <Button
                            variant="outline"
                            size="sm"
                            onClick={() => risk && runAnalysis(risk)}
                            disabled={loading}
                        >
                            {loading ? 'Analyzing...' : 'Refresh Analysis'}
                        </Button>
                    </div>

                    {loading && (
                        <div className="space-y-3">
                            <div className="flex items-center gap-2 text-sm text-muted-foreground">
                                <div className="animate-spin w-4 h-4 border-2 border-primary border-t-transparent rounded-full" />
                                Analyzing risk with AI...
                            </div>
                            {toolsUsed.length > 0 && (
                                <div className="flex flex-wrap gap-2">
                                    {toolsUsed.map((tool, i) => (
                                        <Badge key={i} variant="secondary" className="text-xs">
                                            {tool}
                                        </Badge>
                                    ))}
                                </div>
                            )}
                            <div className="space-y-2">
                                {[1, 2, 3, 4].map(i => (
                                    <div key={i} className="h-4 bg-muted rounded animate-pulse" style={{ width: `${100 - i * 15}%` }} />
                                ))}
                            </div>
                        </div>
                    )}

                    {analysis && !loading && (
                        <div className="bg-muted/50 rounded-lg p-4 border border-border">
                            <div className="prose prose-sm dark:prose-invert max-w-none">
                                <ReactMarkdown
                                    components={{
                                        p: ({ children }) => <p className="mb-3 last:mb-0">{children}</p>,
                                        ul: ({ children }) => <ul className="list-disc pl-4 mb-3">{children}</ul>,
                                        ol: ({ children }) => <ol className="list-decimal pl-4 mb-3">{children}</ol>,
                                        li: ({ children }) => <li className="mb-1">{children}</li>,
                                        strong: ({ children }) => <span className="font-semibold text-primary">{children}</span>,
                                        h1: ({ children }) => <h1 className="text-lg font-bold mb-2 mt-4 first:mt-0">{children}</h1>,
                                        h2: ({ children }) => <h2 className="text-base font-bold mb-2 mt-3 first:mt-0">{children}</h2>,
                                        h3: ({ children }) => <h3 className="text-sm font-bold mb-2 mt-2 first:mt-0">{children}</h3>,
                                    }}
                                >
                                    {analysis}
                                </ReactMarkdown>
                            </div>
                            {toolsUsed.length > 0 && (
                                <div className="mt-4 pt-3 border-t border-border">
                                    <div className="text-xs text-muted-foreground mb-2">Tools used:</div>
                                    <div className="flex flex-wrap gap-1">
                                        {toolsUsed.map((tool, i) => (
                                            <Badge key={i} variant="outline" className="text-xs">
                                                {tool}
                                            </Badge>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </DialogContent>
        </Dialog>
    )
}
