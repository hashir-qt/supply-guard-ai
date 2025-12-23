import { Hero } from '@/components/landing/Hero'
import { DemoVideo } from '@/components/landing/DemoVideo'
import { FeatureGrid } from '@/components/landing/FeatureGrid'

export default function LandingPage() {
    return (
        <div className="flex flex-col">
            <Hero />
            <DemoVideo />
            <FeatureGrid />

            <section className="py-24 px-6 border-t border-slate-200">
                <div className="container mx-auto text-center space-y-8 max-w-3xl">
                    <h2 className="text-4xl font-bold tracking-tight text-slate-900">Ready to secure your supply chain?</h2>
                    <p className="text-xl text-slate-500">
                        Join leading enterprises moving from reactive to predictive planning.
                    </p>
                    <div className="pt-4">
                        <button className="px-8 py-4 bg-slate-900 text-white rounded-full font-medium hover:bg-slate-800 transition-colors shadow-xl">
                            Start Free Pilot
                        </button>
                    </div>
                </div>
            </section>
        </div>
    )
}
