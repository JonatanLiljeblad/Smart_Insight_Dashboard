"use client";

import Link from "next/link";
import type { Favorite } from "@/types/favorite";
import type { Player } from "@/types/player";

interface FavoritesPanelProps {
  favorites: Favorite[];
  players: Player[];
  isLoading: boolean;
}

export default function FavoritesPanel({
  favorites,
  players,
  isLoading,
}: FavoritesPanelProps) {
  const playerMap = new Map(players.map((p) => [p.id, p]));

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
          Star players you want to track — they&apos;ll appear here.
        </p>
      ) : (
        <ul className="space-y-2">
          {favorites.slice(0, 5).map((fav) => {
            const player = playerMap.get(fav.player_id);
            return (
              <li
                key={fav.id}
                className="flex items-center justify-between rounded-lg bg-gray-50 px-4 py-2"
              >
                <div className="min-w-0">
                  <span className="text-sm font-medium text-gray-700 truncate">
                    {player?.name ?? `Player #${fav.player_id}`}
                  </span>
                  {player?.tour && (
                    <span className="ml-2 text-xs text-gray-400">{player.tour}</span>
                  )}
                </div>
                <Link
                  href={`/players/${fav.player_id}`}
                  className="shrink-0 text-xs font-medium text-blue-600 hover:text-blue-500"
                >
                  View
                </Link>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}
