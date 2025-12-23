import { ShieldAlert, Zap, GitBranch } from 'lucide-react'

const features = [
    {
        title: "Predictive Risk Scoring",
        description: "AI-driven analysis of supply chain vulnerabilities. We quantify risks (0-100) across suppliers, logistics, and geopolitics.",
        icon: ShieldAlert,
        color: "text-red-500",
        bg: "bg-red-50",
    },
    {
        title: "Early Warning System",
        description: "Get alerted 30-60 days in advance. Our models process global signal data to forecast potential disruptions before they impact you.",
        icon: Zap,
        color: "text-amber-500",
        bg: "bg-amber-50",
    },
    {
        title: "Mitigation Engine",
        description: "Don't just watch, act. Receive automated recommendations for inventory rebalancing, alternate suppliers, and route optimization.",
        icon: GitBranch,
        color: "text-blue-500",
        bg: "bg-blue-50",
    },
]

export function FeatureGrid() {
    return (
        <section id="features" className="py-24 px-6 bg-slate-50/50">
            <div className="container mx-auto max-w-6xl">
                <div className="text-center mb-16 space-y-4">
                    <h2 className="text-3xl font-bold tracking-tight text-slate-900">Intelligence at Scale</h2>
                    <p className="text-slate-500 text-lg max-w-2xl mx-auto">
                        Built for complexities of global supply chains.
                    </p>
                </div>

                <div className="grid md:grid-cols-3 gap-8">
                    {features.map((feature, idx) => (
                        <div key={idx} className="bg-background rounded-2xl p-8 border border-slate-200/60 shadow-sm hover:shadow-md transition-shadow group">
                            <div className={`w-12 h-12 ${feature.bg} rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300`}>
                                <feature.icon className={`w-6 h-6 ${feature.color}`} />
                            </div>
                            <h3 className="text-xl font-semibold text-slate-900 mb-3">{feature.title}</h3>
                            <p className="text-slate-500 leading-relaxed text-sm">
                                {feature.description}
                            </p>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    )
}
