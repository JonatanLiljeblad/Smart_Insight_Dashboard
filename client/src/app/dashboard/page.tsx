"use client";

import ProtectedRoute from "@/components/auth/protected-route";
import DashboardShell from "@/components/dashboard/dashboard-shell";
import StatCard from "@/components/dashboard/stat-card";
import PlayerTable from "@/components/dashboard/player-table";
import FavoritesPanel from "@/components/dashboard/favorites-panel";
import PlayerTrendChart from "@/components/charts/player-trend-chart";
import { useAuth } from "@/hooks/useAuth";
import { usePlayers, usePlayerStats } from "@/hooks/usePlayers";
import { useFavorites } from "@/hooks/useFavorites";

export default function DashboardPage() {
  const { user } = useAuth();
  const { players, isLoading: playersLoading } = usePlayers();
  const { favorites, isLoading: favoritesLoading } = useFavorites();

  const featuredPlayerId = players.length > 0 ? players[0].id : 0;
  const { stats: featuredStats } = usePlayerStats(featuredPlayerId);

  const tourBreakdown = players.reduce<Record<string, number>>((acc, p) => {
    const tour = p.tour ?? "Other";
    acc[tour] = (acc[tour] || 0) + 1;
    return acc;
  }, {});
  const topTour = Object.entries(tourBreakdown).sort((a, b) => b[1] - a[1])[0];

  return (
    <ProtectedRoute>
      <DashboardShell>
        {/* Welcome */}
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-gray-900">
            Welcome back, {user?.full_name?.split(" ")[0]}
          </h1>
          <p className="mt-1 text-sm text-gray-500">
            Here&apos;s your golf analytics overview.
          </p>
        </div>

        {/* Stat cards */}
        <div className="mb-8 grid grid-cols-1 gap-4 sm:grid-cols-4">
          <StatCard
            label="Total Players"
            value={players.length}
            icon="🏌️"
          />
          <StatCard
            label="Your Favorites"
            value={favorites.length}
            icon="⭐"
          />
          <StatCard
            label="Stat Records"
            value={featuredStats.length > 0 ? `${players.length * 12}+` : "—"}
            icon="📊"
          />
          <StatCard
            label="Top Tour"
            value={topTour ? topTour[0] : "—"}
            icon="🏆"
          />
        </div>

        {/* Featured chart */}
        {players.length > 0 && featuredStats.length > 0 && (
          <div className="mb-8 rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
            <div className="mb-4 flex items-center justify-between">
              <div>
                <h2 className="text-lg font-semibold text-gray-900">
                  Featured Player Trend
                </h2>
                <p className="text-sm text-gray-500">
                  {players[0].name} — scoring average &amp; strokes gained
                </p>
              </div>
            </div>
            <PlayerTrendChart stats={featuredStats} />
          </div>
        )}

        {/* Content grid */}
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          <div className="lg:col-span-2">
            <h2 className="mb-4 text-lg font-semibold text-gray-900">
              Players
            </h2>
            <PlayerTable players={players} isLoading={playersLoading} />
          </div>
          <div>
            <FavoritesPanel
              favorites={favorites}
              players={players}
              isLoading={favoritesLoading}
            />
          </div>
        </div>
      </DashboardShell>
    </ProtectedRoute>
  );
}
