import { Badge } from '@/components/ui/badge'
import { RiskSeverity } from '@/lib/types'

export function SeverityBadge({ severity }: { severity: RiskSeverity | string }) {
    const getVariant = (s: string) => {
        switch (s.toLowerCase()) {
            case 'critical': return 'destructive'
            case 'high': return 'destructive'
            case 'medium': return 'default' // Or a specific orange variant if available, but default/secondary usually fine. Using default for now or I can use custom classes.
            case 'low': return 'secondary'
            default: return 'outline'
        }
    }

    const getColorClass = (s: string) => {
        switch (s.toLowerCase()) {
            case 'critical': return 'bg-red-900 text-red-100 hover:bg-red-800'
            case 'high': return 'bg-red-600 text-white hover:bg-red-500'
            case 'medium': return 'bg-orange-500 text-white hover:bg-orange-400'
            case 'low': return 'bg-green-500 text-white hover:bg-green-400'
            default: return 'bg-gray-500 text-white'
        }
    }

    // Determine if using Shadcn Badge variants or custom classes is better. 
    // Shadcn badges usually have variants: default, secondary, destructive, outline.
    // 'critical' -> destructive
    // 'high' -> destructive? or custom?
    // Let's use custom classes via className to match the dark theme exact colors if needed, or just variants.
    // The provided code implies standard shadcn usage. Let's stick to simple variants for now or custom classes.

    return (
        <Badge className={getColorClass(severity)}>
            {severity.charAt(0).toUpperCase() + severity.slice(1)}
        </Badge>
    )
}
