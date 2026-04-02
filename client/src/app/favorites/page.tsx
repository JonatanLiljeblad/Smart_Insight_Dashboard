"use client";

import ProtectedRoute from "@/components/auth/protected-route";
import DashboardShell from "@/components/dashboard/dashboard-shell";
import Button from "@/components/ui/button";
import { useFavorites } from "@/hooks/useFavorites";
import { usePlayers } from "@/hooks/usePlayers";
import Link from "next/link";

export default function FavoritesPage() {
  const { favorites, isLoading, removeFavorite } = useFavorites();
  const { players } = usePlayers();
  const playerMap = new Map(players.map((p) => [p.id, p]));

  return (
    <ProtectedRoute>
      <DashboardShell>
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-gray-900">Your Favorites</h1>
          <p className="mt-1 text-sm text-gray-500">
            Players you&apos;re tracking. Click to view detailed analytics.
          </p>
        </div>

        {isLoading && (
          <p className="text-sm text-gray-500">Loading favorites…</p>
        )}

        {!isLoading && favorites.length === 0 && (
          <div className="rounded-xl border border-gray-200 bg-white p-12 text-center">
            <span className="text-4xl">⭐</span>
            <p className="mt-4 font-medium text-gray-700">No favorites yet</p>
            <p className="mt-1 text-sm text-gray-500">
              Browse players and star the ones you want to follow.
            </p>
            <Link
              href="/dashboard"
              className="mt-4 inline-block text-sm font-medium text-blue-600 hover:text-blue-500"
            >
              Browse players →
            </Link>
          </div>
        )}

        {!isLoading && favorites.length > 0 && (
          <div className="space-y-3">
            {favorites.map((fav) => {
              const player = playerMap.get(fav.player_id);
              return (
                <div
                  key={fav.id}
                  className="flex items-center justify-between rounded-xl border border-gray-200 bg-white px-6 py-4 shadow-sm"
                >
                  <div className="min-w-0">
                    <Link
                      href={`/players/${fav.player_id}`}
                      className="font-medium text-gray-900 hover:text-blue-600"
                    >
                      {player?.name ?? `Player #${fav.player_id}`}
                    </Link>
                    <div className="flex items-center gap-3 text-xs text-gray-400">
                      {player?.nationality && <span>{player.nationality}</span>}
                      {player?.tour && <span>{player.tour}</span>}
                      <span>
                        Added{" "}
                        {new Date(fav.created_at).toLocaleDateString("en-US", {
                          month: "short",
                          day: "numeric",
                          year: "numeric",
                        })}
                      </span>
                    </div>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => removeFavorite(fav.id)}
                  >
                    Remove
                  </Button>
                </div>
              );
            })}
          </div>
        )}
      </DashboardShell>
    </ProtectedRoute>
  );
}
