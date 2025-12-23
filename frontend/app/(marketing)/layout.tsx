import { Navbar } from '@/components/landing/Navbar'

export default function MarketingLayout({ children }: { children: React.ReactNode }) {
    return (
        <div className="min-h-screen bg-background text-foreground flex flex-col">
            <Navbar />
            <main className="flex-1 flex flex-col">
                {children}
            </main>
            <footer className="border-t border-border py-12 mt-auto bg-slate-50">
                <div className="container mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-6 text-sm text-muted-foreground">
                    <p>© 2025 SupplyGuard AI. All rights reserved.</p>
                    <div className="flex gap-6">
                        <a href="#" className="hover:text-foreground">Privacy</a>
                        <a href="#" className="hover:text-foreground">Terms</a>
                        <a href="#" className="hover:text-foreground">Twitter</a>
                    </div>
                </div>
            </footer>
        </div>
    )
}
