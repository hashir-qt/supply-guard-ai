'use client'
import { useState } from 'react'
import { Send } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

interface Props {
    onSend: (message: string) => void
    disabled?: boolean
}

export function ChatInput({ onSend, disabled }: Props) {
    const [input, setInput] = useState('')

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault()
        if (input.trim()) {
            onSend(input)
            setInput('')
        }
    }

    return (
        <form onSubmit={handleSubmit} className="p-4 border-t border-border flex gap-2 bg-background">
            <Input
                value={input}
                onChange={e => setInput(e.target.value)}
                placeholder="Ask about risks..."
                className="bg-muted border-input focus-visible:ring-ring"
                disabled={disabled}
            />
            <Button type="submit" size="icon" disabled={disabled || !input.trim()}>
                <Send className="w-4 h-4" />
            </Button>
        </form>
    )
}
