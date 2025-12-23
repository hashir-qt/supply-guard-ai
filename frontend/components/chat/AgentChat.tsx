'use client'
import { useState } from 'react'
import { api } from '@/lib/api'
import { ChatMessages } from './ChatMessages'
import { ChatInput } from './ChatInput'
import { ToolIndicator } from './ToolIndicator'

export function AgentChat() {
    const [messages, setMessages] = useState<Array<{ role: string, content: string }>>([])
    const [loading, setLoading] = useState(false)
    const [toolsUsed, setToolsUsed] = useState<string[]>([])

    const sendMessage = async (message: string) => {
        setMessages(prev => [...prev, { role: 'user', content: message }])
        setLoading(true)
        setToolsUsed([])

        try {
            // Direct call or stream? Instructions say chat but code in prompt snippet used "api.agent.chat"
            const response = await api.agent.chat(message)
            setMessages(prev => [...prev, { role: 'assistant', content: response.response }])
            setToolsUsed(response.tools_used)
        } catch (error) {
            setMessages(prev => [...prev, { role: 'assistant', content: 'Sorry, I encountered an error.' }])
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="flex flex-col h-full bg-card rounded-xl border border-border overflow-hidden">
            <div className="p-4 border-b border-border font-semibold flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                AI Risk Assistant
            </div>

            <div className="flex-1 overflow-hidden relative">
                {messages.length === 0 ? (
                    <div className="absolute inset-0 flex flex-col items-center justify-center text-center p-8 text-muted-foreground">
                        <p className="mb-6 text-lg">👋 Hi Ahmed! Ask me about supply chain risks.</p>
                        <div className="space-y-3 max-w-xs w-full">
                            <button
                                onClick={() => sendMessage("What are our top risks right now?")}
                                className="w-full text-left px-4 py-3 rounded-lg bg-muted hover:bg-muted/80 transition-colors text-sm text-foreground border border-border"
                            >
                                "What are our top risks right now?"
                            </button>
                            <button
                                onClick={() => sendMessage("How's our chicken supply?")}
                                className="w-full text-left px-4 py-3 rounded-lg bg-muted hover:bg-muted/80 transition-colors text-sm text-foreground border border-border"
                            >
                                "How's our chicken supply?"
                            </button>
                        </div>
                    </div>
                ) : (
                    <ChatMessages messages={messages} />
                )}
            </div>

            {loading && <ToolIndicator tools={toolsUsed.length > 0 ? toolsUsed : ['Processing...']} />}
            <ChatInput onSend={sendMessage} disabled={loading} />
        </div>
    )
}
