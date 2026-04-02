"use client";

import Link from "next/link";
import type { Favorite } from "@/types/favorite";

interface FavoritesPanelProps {
  favorites: Favorite[];
  isLoading: boolean;
}

export default function FavoritesPanel({
  favorites,
  isLoading,
}: FavoritesPanelProps) {
  if (isLoading) {
    return (
      <div className="rounded-xl border border-gray-200 bg-white p-6">
        <h3 className="mb-3 text-lg font-semibold text-gray-900">Favorites</h3>
        <p className="text-sm text-gray-500">Loading…</p>
      </div>
    );
  }

  return (
    <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
      <div className="mb-4 flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-900">Favorites</h3>
        <Link
          href="/favorites"
          className="text-sm font-medium text-blue-600 hover:text-blue-500"
        >
          View all
        </Link>
      </div>
      {favorites.length === 0 ? (
        <p className="text-sm text-gray-500">
          No favorites yet. Browse players and add some!
        </p>
      ) : (
        <ul className="space-y-2">
          {favorites.slice(0, 5).map((fav) => (
            <li
              key={fav.id}
              className="flex items-center justify-between rounded-lg bg-gray-50 px-4 py-2"
            >
              <span className="text-sm font-medium text-gray-700">
                Player #{fav.player_id}
              </span>
              <Link
                href={`/players/${fav.player_id}`}
                className="text-xs font-medium text-blue-600 hover:text-blue-500"
              >
                View
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
