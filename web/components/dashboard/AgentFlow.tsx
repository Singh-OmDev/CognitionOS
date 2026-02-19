"use client"

import { useMemo } from 'react';
import ReactFlow, {
    Handle,
    Position,
    Background,
    Controls,
    NodeProps
} from 'reactflow';
import 'reactflow/dist/style.css';
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { GitBranch } from "lucide-react"

// Custom Node for Active Agent
const AgentNode = ({ data }: NodeProps) => {
    return (
        <div className={`px-4 py-2 shadow-md rounded-md bg-white dark:bg-slate-900 border-2 ${data.active ? 'border-indigo-500 animate-pulse' : 'border-slate-200 dark:border-slate-800'}`}>
            <Handle type="target" position={Position.Top} className="!bg-slate-500" />
            <div className="font-bold text-xs">{data.label}</div>
            <div className="text-[10px] text-slate-500">{data.role}</div>
            <Handle type="source" position={Position.Bottom} className="!bg-slate-500" />
        </div>
    );
};

const nodeTypes = { agent: AgentNode };

interface AgentFlowProps {
    currentAgent?: string
}

export function AgentFlow({ currentAgent }: AgentFlowProps) {

    const nodes = useMemo(() => [
        { id: 'start', type: 'input', data: { label: 'Start' }, position: { x: 250, y: 0 } },
        { id: 'planner', type: 'agent', data: { label: 'Planner', role: 'Decompose', active: currentAgent === 'Planner' }, position: { x: 250, y: 80 } },
        { id: 'researcher', type: 'agent', data: { label: 'Researcher', role: 'Search', active: currentAgent === 'Researcher' }, position: { x: 100, y: 200 } },
        { id: 'coder', type: 'agent', data: { label: 'Coder', role: 'Implement', active: currentAgent === 'Coder' }, position: { x: 400, y: 200 } },
        { id: 'critic', type: 'agent', data: { label: 'Critic', role: 'Review', active: currentAgent === 'Critic' }, position: { x: 250, y: 320 } },
        { id: 'end', type: 'output', data: { label: 'End' }, position: { x: 250, y: 420 } },
    ], [currentAgent]);

    const edges = useMemo(() => [
        { id: 'e1-2', source: 'start', target: 'planner', animated: true },
        { id: 'e2-3', source: 'planner', target: 'researcher', animated: true },
        { id: 'e2-4', source: 'planner', target: 'coder', animated: true },
        { id: 'e3-5', source: 'researcher', target: 'critic', animated: true },
        { id: 'e4-5', source: 'coder', target: 'critic', animated: true },
        { id: 'e5-6', source: 'critic', target: 'end', animated: currentAgent === 'Critic' },
        { id: 'e5-2', source: 'critic', target: 'planner', label: 'Retry', animated: true, style: { stroke: '#f59e0b' } },
    ], [currentAgent]);

    return (
        <Card className="h-full flex flex-col">
            <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium flex items-center gap-2">
                    <GitBranch className="w-4 h-4 text-indigo-500" />
                    Execution Graph
                </CardTitle>
            </CardHeader>
            <CardContent className="flex-1 min-h-[200px] p-0 relative">
                <div style={{ width: '100%', height: '100%' }}>
                    <ReactFlow
                        nodes={nodes}
                        edges={edges}
                        nodeTypes={nodeTypes}
                        fitView
                        proOptions={{ hideAttribution: true }}
                    >
                        <Background color="#94a3b8" gap={16} size={1} />
                    </ReactFlow>
                </div>
            </CardContent>
        </Card>
    )
}
