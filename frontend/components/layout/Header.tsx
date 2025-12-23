'use client'
import { Bell, Search } from 'lucide-react'
import { Badge } from '@/components/ui/badge'

export function Header() {
    return (
        <header className="h-16 border-b border-border bg-background flex items-center justify-between px-6">
            {/* Search */}
            <div className="flex-1 max-w-xl">
                <div className="relative">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                    <input
                        type="text"
                        placeholder="Search risks, suppliers, outlets..."
                        className="w-full bg-gray-800 border border-gray-700 rounded-lg pl-10 pr-4 py-2 text-sm focus:outline-none focus:border-blue-500"
                    />
                </div>
            </div>

            {/* Right side */}
            <div className="flex items-center gap-4">
                <button className="relative">
                    <Bell className="w-5 h-5 text-gray-400 hover:text-white" />
                    <Badge className="absolute -top-1 -right-1 h-4 w-4 p-0 flex items-center justify-center text-xs bg-red-600">
                        8
                    </Badge>
                </button>
                <div className="text-sm text-gray-400">
                    Last updated: <span className="text-white">2 min ago</span>
                </div>
            </div>
        </header>
    )
}
