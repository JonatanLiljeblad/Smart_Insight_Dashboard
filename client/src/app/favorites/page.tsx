"use client";

import ProtectedRoute from "@/components/auth/protected-route";
import DashboardShell from "@/components/dashboard/dashboard-shell";
import Button from "@/components/ui/button";
import { useFavorites } from "@/hooks/useFavorites";
import Link from "next/link";

export default function FavoritesPage() {
  const { favorites, isLoading, removeFavorite } = useFavorites();

  return (
    <ProtectedRoute>
      <DashboardShell>
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-gray-900">Your Favorites</h1>
          <p className="mt-1 text-sm text-gray-500">
            Players you&apos;re tracking.
          </p>
        </div>

        {isLoading && (
          <p className="text-sm text-gray-500">Loading favorites…</p>
        )}

        {!isLoading && favorites.length === 0 && (
          <div className="rounded-xl border border-gray-200 bg-white p-12 text-center">
            <p className="text-gray-500">No favorites yet.</p>
            <Link
              href="/dashboard"
              className="mt-2 inline-block text-sm font-medium text-blue-600 hover:text-blue-500"
            >
              Browse players →
            </Link>
          </div>
        )}

        {!isLoading && favorites.length > 0 && (
          <div className="space-y-3">
            {favorites.map((fav) => (
              <div
                key={fav.id}
                className="flex items-center justify-between rounded-xl border border-gray-200 bg-white px-6 py-4 shadow-sm"
              >
                <div>
                  <Link
                    href={`/players/${fav.player_id}`}
                    className="font-medium text-gray-900 hover:text-blue-600"
                  >
                    Player #{fav.player_id}
                  </Link>
                  <p className="text-xs text-gray-400">
                    Added{" "}
                    {new Date(fav.created_at).toLocaleDateString("en-US", {
                      month: "short",
                      day: "numeric",
                      year: "numeric",
                    })}
                  </p>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => removeFavorite(fav.id)}
                >
                  Remove
                </Button>
              </div>
            ))}
          </div>
        )}
      </DashboardShell>
    </ProtectedRoute>
  );
}
