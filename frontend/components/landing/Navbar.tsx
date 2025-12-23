import Link from 'next/link'
import { Button } from '@/components/ui/button'

export function Navbar() {
    return (
        <nav className="fixed top-0 w-full z-50 bg-background/80 backdrop-blur-md border-b border-border/40">
            <div className="container mx-auto px-6 h-16 flex items-center justify-between">
                <div className="flex items-center gap-8">
                    <Link href="/" className="font-bold text-xl flex items-center gap-2">
                        <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-white">
                            S
                        </div>
                        <span>Supply Guard AI</span>
                    </Link>

                    <div className="hidden md:flex items-center gap-6 text-sm font-medium text-muted-foreground">
                        <Link href="#features" className="hover:text-foreground transition-colors">Features</Link>
                        <Link href="#how-it-works" className="hover:text-foreground transition-colors">How it works</Link>
                        <Link href="#pricing" className="hover:text-foreground transition-colors">Pricing</Link>
                    </div>
                </div>

                <div className="flex items-center gap-4">
                    <Link href="/login" className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">
                        Sign in
                    </Link>
                    <Link href="/dashboard">
                        <Button size="sm" className="bg-blue-600 hover:bg-blue-700 text-white">
                            Get Started
                        </Button>
                    </Link>
                </div>
            </div>
        </nav>
    )
}
