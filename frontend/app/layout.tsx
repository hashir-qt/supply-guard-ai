import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
    title: 'SupplyGuard AI - KFC Pakistan',
    description: 'AI-powered supply chain risk intelligence',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
    return (
        <html lang="en">
            <body className={`${inter.className} bg-background text-foreground`}>
                {children}
            </body>
        </html>
    )
}
