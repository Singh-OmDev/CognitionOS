"use client"

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Database, FolderOpen, History, Lightbulb } from "lucide-react"

interface MemoryInspectorProps {
    memorySnapshot?: any
}

export function MemoryInspector({ memorySnapshot }: MemoryInspectorProps) {
    return (
        <Card className="h-full flex flex-col">
            <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium flex items-center gap-2">
                    <Database className="w-4 h-4 text-blue-500" />
                    Memory Matrix
                </CardTitle>
            </CardHeader>
            <CardContent className="flex-1 p-2">
                <Tabs defaultValue="semantic" className="w-full h-full flex flex-col">
                    <TabsList className="grid w-full grid-cols-4">
                        <TabsTrigger value="semantic"><Lightbulb className="w-3 h-3 mr-1" /> Semantic</TabsTrigger>
                        <TabsTrigger value="episodic"><History className="w-3 h-3 mr-1" /> Episodic</TabsTrigger>
                        <TabsTrigger value="tool"><FolderOpen className="w-3 h-3 mr-1" /> Tool</TabsTrigger>
                    </TabsList>

                    <div className="mt-2 flex-1 bg-slate-50 dark:bg-slate-900 rounded-md p-2 overflow-auto text-xs font-mono">
                        <TabsContent value="semantic" className="m-0">
                            {/* Placeholder for Semantic Vector Search Results */}
                            <div className="text-slate-500 italic">No contexts retrieved yet.</div>
                        </TabsContent>
                        <TabsContent value="episodic" className="m-0">
                            {/* Placeholder for Task History */}
                            <div className="text-slate-500 italic">No past episodes loaded.</div>
                        </TabsContent>
                        <TabsContent value="tool" className="m-0">
                            {/* Placeholder for Tool Stats */}
                            <pre>{JSON.stringify(memorySnapshot?.tools || {}, null, 2)}</pre>
                        </TabsContent>
                    </div>
                </Tabs>
            </CardContent>
        </Card>
    )
}
