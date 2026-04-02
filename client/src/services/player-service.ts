import { apiFetch } from "@/lib/api";
import type { Player } from "@/types/player";

export function getPlayers(skip = 0, limit = 20): Promise<Player[]> {
  return apiFetch<Player[]>(`/api/players/?skip=${skip}&limit=${limit}`);
}

export function getPlayer(id: number): Promise<Player> {
  return apiFetch<Player>(`/api/players/${id}`);
}
