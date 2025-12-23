'use client'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { LayoutDashboard, AlertTriangle, Factory, Store, Truck, FlaskConical, Calendar, History } from 'lucide-react'

const navItems = [
    { href: '/dashboard', label: 'Overview', icon: LayoutDashboard },
    { href: '/dashboard/risks', label: 'Risks', icon: AlertTriangle },
    { href: '/dashboard/suppliers', label: 'Suppliers', icon: Factory },
    { href: '/dashboard/outlets', label: 'Outlets', icon: Store },
    { href: '/dashboard/simulation', label: 'Simulator', icon: FlaskConical },
]

export function Sidebar() {
    const pathname = usePathname()

    return (
        <aside className="w-64 bg-sidebar border-r border-sidebar-border flex flex-col">
            {/* Logo */}
            <div className="p-6 border-b border-gray-800">
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-red-600 rounded-lg flex items-center justify-center">
                        <span className="text-white font-bold text-xl">🍗</span>
                    </div>
                    <Link href="/">
                        <div>
                            <h1 className="font-bold text-lg">Supply Guard AI</h1>
                            <p className="text-xs text-gray-400">KFC Pakistan</p>
                        </div>
                    </Link>
                </div>
            </div>

            {/* Navigation */}
            <nav className="flex-1 p-4 space-y-1">
                {navItems.map((item) => {
                    const Icon = item.icon
                    const isActive = pathname === item.href
                    return (
                        <Link
                            key={item.href}
                            href={item.href}
                            className={`flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${isActive
                                ? 'bg-blue-600 text-white'
                                : 'text-gray-400 hover:bg-gray-800 hover:text-white'
                                }`}
                        >
                            <Icon className="w-5 h-5" />
                            <span>{item.label}</span>
                        </Link>
                    )
                })}
            </nav>

            {/* User */}
            <div className="p-4 border-t border-gray-800">
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-gray-800 rounded-full flex items-center justify-center">
                        <span className="text-sm">AM</span>
                    </div>
                    <div>
                        <p className="text-sm font-medium">Ahmed</p>
                        <p className="text-xs text-gray-400">Supply Chain Manager</p>
                    </div>
                </div>
            </div>
        </aside>
    )
}
