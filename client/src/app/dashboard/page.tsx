"use client";

import ProtectedRoute from "@/components/auth/protected-route";
import DashboardShell from "@/components/dashboard/dashboard-shell";
import StatCard from "@/components/dashboard/stat-card";
import PlayerTable from "@/components/dashboard/player-table";
import FavoritesPanel from "@/components/dashboard/favorites-panel";
import { useAuth } from "@/hooks/useAuth";
import { usePlayers } from "@/hooks/usePlayers";
import { useFavorites } from "@/hooks/useFavorites";

export default function DashboardPage() {
  const { user } = useAuth();
  const { players, isLoading: playersLoading } = usePlayers();
  const { favorites, isLoading: favoritesLoading } = useFavorites();

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
        <div className="mb-8 grid grid-cols-1 gap-4 sm:grid-cols-3">
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
          <StatCard label="Data Points" value="—" icon="📊" />
        </div>

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
              isLoading={favoritesLoading}
            />
          </div>
        </div>
      </DashboardShell>
    </ProtectedRoute>
  );
}
