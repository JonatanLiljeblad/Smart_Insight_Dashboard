"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import type { PlayerStat } from "@/types/player";

interface PlayerTrendChartProps {
  stats: PlayerStat[];
}

export default function PlayerTrendChart({ stats }: PlayerTrendChartProps) {
  if (stats.length === 0) {
    return (
      <div className="flex h-64 items-center justify-center rounded-xl border border-gray-200 bg-white text-sm text-gray-500">
        No stats data available yet.
      </div>
    );
  }

  const chartData = stats
    .sort(
      (a, b) =>
        new Date(a.event_date).getTime() - new Date(b.event_date).getTime(),
    )
    .map((s) => ({
      date: s.event_date,
      scoring: s.scoring_average,
      sg: s.strokes_gained_total,
    }));

  return (
    <div className="h-64 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis dataKey="date" tick={{ fontSize: 12 }} stroke="#9ca3af" />
          <YAxis tick={{ fontSize: 12 }} stroke="#9ca3af" />
          <Tooltip />
          <Line
            type="monotone"
            dataKey="scoring"
            name="Scoring Avg"
            stroke="#2563eb"
            strokeWidth={2}
            dot={{ r: 3 }}
          />
          <Line
            type="monotone"
            dataKey="sg"
            name="Strokes Gained"
            stroke="#16a34a"
            strokeWidth={2}
            dot={{ r: 3 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
