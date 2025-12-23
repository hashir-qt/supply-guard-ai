import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { ArrowRight, Download } from 'lucide-react'

export function Hero() {
    return (
        <section className="pt-32 pb-16 md:pt-48 md:pb-32 px-6 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-blue-50/50 via-background to-background">
            <div className="container mx-auto max-w-5xl text-center space-y-8">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 text-blue-700 text-xs font-medium border border-blue-100 mb-4 animate-in fade-in slide-in-from-bottom-4 duration-700">
                    <span className="relative flex h-2 w-2">
                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
                        <span className="relative inline-flex rounded-full h-2 w-2 bg-blue-500"></span>
                    </span>
                    One AI Hackathon 2025 Winner
                </div>

                <h1 className="text-5xl md:text-7xl font-bold tracking-tight text-slate-900 animate-in fade-in slide-in-from-bottom-6 duration-700">
                    Predict Disruptions <br />
                    <span className="text-blue-600">Before They Happen</span>
                </h1>

                <p className="text-xl text-slate-600 max-w-2xl mx-auto leading-relaxed animate-in fade-in slide-in-from-bottom-8 duration-700 delay-100">
                    SupplyGuard AI is an AI-powered supply chain intelligence system.
                    We move beyond reactive planning to give you <span className="font-semibold text-slate-900">30-60 day predictive visibility</span>.
                </p>

                <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4 animate-in fade-in slide-in-from-bottom-10 duration-700 delay-200">
                    <Link href="/dashboard">
                        <Button size="lg" className="h-12 px-8 text-base bg-blue-600 hover:bg-blue-700 text-white rounded-full shadow-lg shadow-blue-200/50 transition-all hover:scale-105">
                            Get Early Access <ArrowRight className="ml-2 w-4 h-4" />
                        </Button>
                    </Link>
                    <Button variant="outline" size="lg" className="h-12 px-8 text-base rounded-full hover:bg-slate-50">
                        View Documentation
                    </Button>
                </div>

                <div className="pt-8 text-xs text-slate-400">
                    Available for Web, iOS, and Android
                </div>
            </div>
        </section>
    )
}
