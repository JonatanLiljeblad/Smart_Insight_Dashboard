"use client";

import { use } from "react";
import ProtectedRoute from "@/components/auth/protected-route";
import DashboardShell from "@/components/dashboard/dashboard-shell";
import PlayerTrendChart from "@/components/charts/player-trend-chart";
import Button from "@/components/ui/button";
import { usePlayer } from "@/hooks/usePlayers";
import { useFavorites } from "@/hooks/useFavorites";

export default function PlayerDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = use(params);
  const playerId = parseInt(id, 10);
  const { player, isLoading, error } = usePlayer(playerId);
  const { favorites, addFavorite, removeFavorite } = useFavorites();

  const existingFav = favorites.find((f) => f.player_id === playerId);

  async function toggleFavorite() {
    if (existingFav) {
      await removeFavorite(existingFav.id);
    } else {
      await addFavorite(playerId);
    }
  }

  return (
    <ProtectedRoute>
      <DashboardShell>
        {isLoading && <p className="text-sm text-gray-500">Loading…</p>}
        {error && <p className="text-sm text-red-600">{error}</p>}
        {player && (
          <div className="space-y-8">
            {/* Header */}
            <div className="flex items-start justify-between">
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  {player.name}
                </h1>
                <div className="mt-1 flex gap-3 text-sm text-gray-500">
                  {player.nationality && <span>{player.nationality}</span>}
                  {player.tour && (
                    <span className="rounded-full bg-blue-50 px-2 py-0.5 text-xs font-medium text-blue-700">
                      {player.tour}
                    </span>
                  )}
                </div>
              </div>
              <Button
                variant={existingFav ? "danger" : "secondary"}
                size="sm"
                onClick={toggleFavorite}
              >
                {existingFav ? "Remove favorite" : "⭐ Add favorite"}
              </Button>
            </div>

            {/* Chart */}
            <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
              <h2 className="mb-4 text-lg font-semibold text-gray-900">
                Performance Trend
              </h2>
              <PlayerTrendChart stats={[]} />
            </div>

            {/* Player info */}
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
              <div className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
                <p className="text-sm font-medium text-gray-500">
                  External ID
                </p>
                <p className="mt-1 font-mono text-sm text-gray-900">
                  {player.external_id}
                </p>
              </div>
              <div className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
                <p className="text-sm font-medium text-gray-500">
                  Nationality
                </p>
                <p className="mt-1 text-sm text-gray-900">
                  {player.nationality ?? "—"}
                </p>
              </div>
              <div className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
                <p className="text-sm font-medium text-gray-500">Tour</p>
                <p className="mt-1 text-sm text-gray-900">
                  {player.tour ?? "—"}
                </p>
              </div>
            </div>
          </div>
        )}
      </DashboardShell>
    </ProtectedRoute>
  );
}
