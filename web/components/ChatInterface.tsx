"use client"

import { useState, useRef, useEffect } from "react"
// Note: These components will be installed by shadcn later
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { Bot, User, Brain, AlertCircle, CheckCircle2, Loader2, Sparkles } from "lucide-react"

interface LogStep {
    thought?: string
    tool?: string
    tool_input?: string
    tool_output?: string
    code?: string
    code_output?: string
    critique?: string
    reflection?: string
    lesson?: string
    error?: string
}

interface Message {
    role: "user" | "assistant"
    content: string
    steps?: LogStep[]
}

interface ChatInterfaceProps {
    onLogUpdate?: (log: any) => void
    onConfidenceUpdate?: (step: number, confidence: number) => void
    onAgentUpdate?: (agent: string) => void
}

export function ChatInterface({ onLogUpdate, onConfidenceUpdate, onAgentUpdate }: ChatInterfaceProps) {
    const [query, setQuery] = useState("")
    const [messages, setMessages] = useState<Message[]>([])
    const [isLoading, setIsLoading] = useState(false)
    const [currentStep, setCurrentStep] = useState<LogStep | null>(null)

    const scrollRef = useRef<HTMLDivElement>(null)

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollIntoView({ behavior: "smooth" })
        }
    }, [messages, currentStep])

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        if (!query.trim() || isLoading) return

        const userMsg: Message = { role: "user", content: query }
        setMessages(prev => [...prev, userMsg])
        setQuery("")
        setIsLoading(true)
        setCurrentStep(null)

        // Append empty assistant message to hold partial updates
        setMessages(prev => [...prev, { role: "assistant", content: "", steps: [] }])

        try {
            // Connect to SSE Endpoint
            // Ensure specific port if needed or use environment var
            const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
            const res = await fetch(`${apiUrl}/task/stream`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query: userMsg.content }),
            })

            if (!res.body) throw new Error("No response body")

            const reader = res.body.getReader()
            const decoder = new TextDecoder()

            let loop = true
            while (loop) {
                const { done, value } = await reader.read()
                if (done) break

                const chunk = decoder.decode(value)
                const lines = chunk.split("\n\n")

                for (const line of lines) {
                    if (line.startsWith("data: ")) {
                        const dataStr = line.replace("data: ", "").trim()
                        if (dataStr === "[DONE]") {
                            loop = false
                            break
                        }

                        try {
                            const data = JSON.parse(dataStr)

                            // Update state based on event type
                            setMessages(prev => {
                                const lastMsg = { ...prev[prev.length - 1] }

                                // Accumulate steps
                                if (!lastMsg.steps) lastMsg.steps = []
                                lastMsg.steps.push(data)

                                // If final response code_output exists, update content
                                if (data.code_output || data.result) {
                                    // Only set content if we have a "final" looking output
                                    // For simplicity, we just use the last meaningful output as content
                                    if (typeof data.code_output === 'string') lastMsg.content = data.code_output
                                    if (typeof data.result === 'string') lastMsg.content = data.result
                                }

                                const newMsgs = [...prev]
                                newMsgs[newMsgs.length - 1] = lastMsg
                                return newMsgs
                            })

                            setCurrentStep(data)

                            // Update Dashboard
                            if (onLogUpdate) {
                                onLogUpdate({
                                    timestamp: new Date().toLocaleTimeString(),
                                    step: data.step || "Step",
                                    message: data.thought || data.critique || data.lesson || "Processing...",
                                    data: data
                                })
                            }
                            if (onConfidenceUpdate && data.confidence) {
                                onConfidenceUpdate(data.step || 0, data.confidence)
                            }
                            if (onAgentUpdate && data.current_agent) {
                                onAgentUpdate(data.current_agent)
                            }
                        } catch (e) {
                            console.error("Error parsing SSE JSON", e)
                        }
                    }
                }
            }

        } catch (err) {
            console.error(err)
            setMessages(prev => [...prev, { role: "assistant", content: `Error: ${err}` }])
        } finally {
            setIsLoading(false)
            setCurrentStep(null)
        }
    }

    return (
        <div className="flex flex-col h-screen max-w-4xl mx-auto p-4 gap-4">
            <Card className="flex-1 overflow-hidden flex flex-col shadow-xl border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-slate-950/50 backdrop-blur">
                <CardHeader className="border-b bg-slate-50/50 dark:bg-slate-900/50 pb-4">
                    <CardTitle className="flex items-center gap-2">
                        <Brain className="w-6 h-6 text-indigo-500" />
                        CognitionOS
                        <Badge variant="outline" className="ml-auto font-normal text-xs uppercase tracking-widest text-slate-500">
                            Agentic Workspace
                        </Badge>
                    </CardTitle>
                </CardHeader>

                <ScrollArea className="flex-1 p-4">
                    <div className="flex flex-col gap-6">
                        {messages.map((msg, i) => (
                            <div key={i} className={`flex gap-4 ${msg.role === "user" ? "flex-row-reverse" : ""}`}>
                                <Avatar className={msg.role === "assistant" ? "bg-indigo-100 dark:bg-indigo-900" : "bg-slate-100 dark:bg-slate-800"}>
                                    <AvatarFallback>
                                        {msg.role === "assistant" ? <Bot className="w-5 h-5 text-indigo-600 dark:text-indigo-400" /> : <User className="w-5 h-5 text-slate-600 dark:text-slate-400" />}
                                    </AvatarFallback>
                                </Avatar>

                                <div className={`flex flex-col gap-2 max-w-[80%] ${msg.role === "user" ? "items-end" : "items-start"}`}>
                                    {/* Log Steps (Thoughts) */}
                                    {msg.steps && msg.steps.length > 0 && (
                                        <div className="text-xs space-y-2 mb-2 w-full">
                                            {msg.steps.map((step, si) => (
                                                <div key={si} className="p-3 rounded-lg bg-slate-50 dark:bg-slate-900 border border-slate-100 dark:border-slate-800 animate-in fade-in slide-in-from-bottom-2 duration-300">
                                                    {step.thought && (
                                                        <div className="flex gap-2 text-slate-600 dark:text-slate-400 font-medium">
                                                            <Brain className="w-3 h-3 mt-0.5" />
                                                            {step.thought}
                                                        </div>
                                                    )}
                                                    {step.tool && (
                                                        <div className="mt-2 pl-5 border-l-2 border-indigo-200 dark:border-indigo-800">
                                                            <div className="font-mono text-indigo-600 dark:text-indigo-400">Allowed Tool: {step.tool}</div>
                                                            <div className="text-slate-500 dark:text-slate-500 truncate">{step.tool_input}</div>
                                                        </div>
                                                    )}
                                                    {step.code && (
                                                        <pre className="mt-2 p-2 rounded bg-slate-950 text-slate-50 text-[10px] overflow-x-auto font-mono">
                                                            {step.code}
                                                        </pre>
                                                    )}
                                                    {step.critique && (
                                                        <div className="mt-2 flex gap-2 text-amber-600 dark:text-amber-500 bg-amber-50 dark:bg-amber-950/30 p-2 rounded">
                                                            <AlertCircle className="w-3 h-3 mt-0.5" />
                                                            Critique: {step.critique}
                                                        </div>
                                                    )}
                                                    {step.lesson && (
                                                        <div className="mt-2 flex gap-2 text-emerald-600 dark:text-emerald-500 bg-emerald-50 dark:bg-emerald-950/30 p-2 rounded">
                                                            <Sparkles className="w-3 h-3 mt-0.5" />
                                                            Lesson: {step.lesson}
                                                        </div>
                                                    )}
                                                </div>
                                            ))}
                                        </div>
                                    )}

                                    {/* Final Content */}
                                    {msg.content && (
                                        <div className={`p-4 rounded-xl shadow-sm ${msg.role === "user"
                                            ? "bg-indigo-600 text-white rounded-br-none"
                                            : "bg-white dark:bg-slate-900 border rounded-bl-none prose prose-sm dark:prose-invert max-w-none"
                                            }`}>
                                            {msg.content.split('\n').map((line, li) => (
                                                <div key={li}>{line}</div>
                                            ))}
                                        </div>
                                    )}

                                    {/* Loading State for current step */}
                                    {isLoading && i === messages.length - 1 && !currentStep && (
                                        <div className="flex items-center gap-2 text-xs text-slate-400 animate-pulse">
                                            <Loader2 className="w-3 h-3 animate-spin" />
                                            Thinking...
                                        </div>
                                    )}
                                </div>
                            </div>
                        ))}
                        <div ref={scrollRef} />
                    </div>
                </ScrollArea>

                <CardContent className="p-4 border-t bg-white dark:bg-slate-950">
                    <form onSubmit={handleSubmit} className="flex gap-2">
                        <Input
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                            placeholder="Ask Agent (e.g., 'Research LangChain', 'Write a script')..."
                            disabled={isLoading}
                            className="flex-1"
                        />
                        <Button type="submit" disabled={isLoading || !query.trim()}>
                            {isLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : "Send"}
                        </Button>
                    </form>
                </CardContent>
            </Card>
        </div>
    )
}
