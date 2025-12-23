import { Wrench } from 'lucide-react'
import { Badge } from '@/components/ui/badge'

export function ToolIndicator({ tools }: { tools: string[] }) {
    if (!tools || tools.length === 0) return null

    return (
        <div className="flex flex-wrap gap-2 px-4 py-2 bg-gray-900/50">
            <div className="flex items-center gap-2 text-xs text-gray-400">
                <Wrench className="w-3 h-3" />
                <span>Tools used:</span>
            </div>
            {tools.map(tool => (
                <Badge key={tool} variant="secondary" className="text-[10px] h-5">
                    {tool}
                </Badge>
            ))}
        </div>
    )
}
