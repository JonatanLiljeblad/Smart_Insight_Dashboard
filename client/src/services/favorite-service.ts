import { apiFetch } from "@/lib/api";
import type { Favorite } from "@/types/favorite";

export function getFavorites(): Promise<Favorite[]> {
  return apiFetch<Favorite[]>("/api/favorites/");
}

export function addFavorite(playerId: number): Promise<Favorite> {
  return apiFetch<Favorite>("/api/favorites/", {
    method: "POST",
    body: JSON.stringify({ player_id: playerId }),
  });
}

export function removeFavorite(favoriteId: number): Promise<void> {
  return apiFetch<void>(`/api/favorites/${favoriteId}`, {
    method: "DELETE",
  });
}
