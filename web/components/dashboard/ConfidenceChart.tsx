"use client"

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Activity } from "lucide-react"

interface ConfidenceChartProps {
    data: { step: number; confidence: number }[]
}

export function ConfidenceChart({ data }: ConfidenceChartProps) {
    return (
        <Card className="h-full flex flex-col">
            <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium flex items-center gap-2">
                    <Activity className="w-4 h-4 text-emerald-500" />
                    Confidence Evolution
                </CardTitle>
            </CardHeader>
            <CardContent className="flex-1 min-h-[150px] p-0">
                <div className="w-full h-full min-h-[200px] p-4">
                    <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={data}>
                            <CartesianGrid strokeDasharray="3 3" opacity={0.2} />
                            <XAxis dataKey="step" fontSize={10} tickLine={false} axisLine={false} />
                            <YAxis domain={[0, 1]} fontSize={10} tickLine={false} axisLine={false} />
                            <Tooltip
                                contentStyle={{ borderRadius: '8px', fontSize: '12px' }}
                                itemStyle={{ color: '#10b981' }}
                            />
                            <Line
                                type="monotone"
                                dataKey="confidence"
                                stroke="#10b981"
                                strokeWidth={2}
                                dot={{ r: 3 }}
                                activeDot={{ r: 5 }}
                            />
                        </LineChart>
                    </ResponsiveContainer>
                </div>
            </CardContent>
        </Card>
    )
}
