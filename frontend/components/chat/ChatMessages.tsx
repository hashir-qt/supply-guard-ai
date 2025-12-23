'use client'
import { Card } from '@/components/ui/card'
// import { ScrollArea } from '@/components/ui/scroll-area'
import { cn } from '@/lib/utils'

import ReactMarkdown from 'react-markdown'

interface Message {
    role: string
    content: string
}

export function ChatMessages({ messages }: { messages: Message[] }) {
    return (
        <div className="h-full overflow-y-auto pr-4 pb-2 [&::-webkit-scrollbar]:w-2 [&::-webkit-scrollbar-track]:bg-transparent [&::-webkit-scrollbar-thumb]:bg-gray-200 dark:[&::-webkit-scrollbar-thumb]:bg-gray-700 [&::-webkit-scrollbar-thumb]:rounded-full">
            <div className="space-y-4 p-4">
                {messages.map((msg, i) => (
                    <div
                        key={i}
                        className={cn(
                            "flex w-full",
                            msg.role === 'user' ? "justify-end" : "justify-start"
                        )}
                    >
                        <div
                            className={cn(
                                "rounded-lg px-4 py-2 max-w-[85%] text-sm",
                                msg.role === 'user'
                                    ? "bg-blue-600 text-white"
                                    : "bg-muted text-foreground border border-border"
                            )}
                        >
                            {msg.role === 'user' ? (
                                msg.content
                            ) : (
                                <div className="prose prose-sm dark:prose-invert max-w-none break-words">
                                    <ReactMarkdown
                                        components={{
                                            p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
                                            ul: ({ children }) => <ul className="list-disc pl-4 mb-2">{children}</ul>,
                                            ol: ({ children }) => <ol className="list-decimal pl-4 mb-2">{children}</ol>,
                                            li: ({ children }) => <li className="mb-1">{children}</li>,
                                            strong: ({ children }) => <span className="font-semibold text-primary">{children}</span>,
                                        }}
                                    >
                                        {msg.content}
                                    </ReactMarkdown>
                                </div>
                            )}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    )
}
