"use client"

import { ScrollArea } from "@/components/ui/scroll-area"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Workflow } from "lucide-react"

interface ThoughtStreamProps {
    logs: any[]
}

export function ThoughtStream({ logs }: ThoughtStreamProps) {
    return (
        <Card className="h-full flex flex-col">
            <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium flex items-center gap-2">
                    <Workflow className="w-4 h-4 text-purple-500" />
                    Reflection Stream
                </CardTitle>
            </CardHeader>
            <CardContent className="flex-1 p-0 overflow-hidden">
                <ScrollArea className="h-full p-4">
                    <div className="space-y-4">
                        {logs.map((log, i) => (
                            <div key={i} className="flex gap-3 text-xs">
                                <div className="min-w-[40px] text-slate-400 text-[10px] pt-1">
                                    {log.timestamp || "00:00"}
                                </div>
                                <div className="flex-1 space-y-1">
                                    <div className="font-semibold text-slate-700 dark:text-slate-300">
                                        {log.step || "Step"}
                                    </div>
                                    <div className="text-slate-600 dark:text-slate-400">
                                        {log.message}
                                    </div>
                                    {log.data && (
                                        <pre className="bg-slate-100 dark:bg-slate-900 p-1 rounded text-[10px] overflow-x-auto">
                                            {JSON.stringify(log.data, null, 2)}
                                        </pre>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>
                </ScrollArea>
            </CardContent>
        </Card>
    )
}
