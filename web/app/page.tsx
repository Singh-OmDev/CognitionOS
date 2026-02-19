"use client"

import { useState, useEffect } from "react"
import { ChatInterface } from "@/components/ChatInterface"
import { AgentFlow } from "@/components/dashboard/AgentFlow"
import { MemoryInspector } from "@/components/dashboard/MemoryInspector"
import { ConfidenceChart } from "@/components/dashboard/ConfidenceChart"
import { ThoughtStream } from "@/components/dashboard/ThoughtStream"

export default function Home() {
  // Shared state for Dashboard components
  // In a real app, this would be in a Context or Store (Zustand/Recoil)
  const [currentAgent, setCurrentAgent] = useState("planner")
  const [confidenceData, setConfidenceData] = useState<{ step: number; confidence: number }[]>([])
  const [logs, setLogs] = useState<any[]>([])

  // Mock Data Updates for demo purposes (until real stream integration)
  // real integration happens in ChatInterface, which needs to lift state up
  // For now, we'll keep ChatInterface independent and just show the layout structure

  return (
    <main className="min-h-screen bg-slate-50 dark:bg-slate-950 p-4 font-sans text-slate-900 dark:text-slate-50">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 h-[90vh]">

        {/* Left Column: Chat & Flow (50%) */}
        <div className="lg:col-span-6 flex flex-col gap-4 h-full">
          <div className="flex-[2] min-h-0">
            <ChatInterface
              onLogUpdate={(log) => setLogs(prev => [log, ...prev])}
              onConfidenceUpdate={(step, conf) => setConfidenceData(prev => [...prev, { step, confidence: conf }])}
              onAgentUpdate={setCurrentAgent}
            />
          </div>
          <div className="flex-1 min-h-[300px]">
            <AgentFlow currentAgent={currentAgent} />
          </div>
        </div>

        {/* Right Column: Memory, Stats, Logs (50%) */}
        <div className="lg:col-span-6 flex flex-col gap-4 h-full">
          <div className="flex-1 grid grid-cols-2 gap-4 min-h-[250px]">
            <ConfidenceChart data={confidenceData} />
            <MemoryInspector />
          </div>
          <div className="flex-[2] min-h-0">
            <ThoughtStream logs={logs} />
          </div>
        </div>

      </div>
    </main>
  )
}
