import { apiFetch } from "@/lib/api";
import type { Player, PlayerStat } from "@/types/player";

export function getPlayers(skip = 0, limit = 20): Promise<Player[]> {
  return apiFetch<Player[]>(`/api/players/?skip=${skip}&limit=${limit}`);
}

export function getPlayer(id: number): Promise<Player> {
  return apiFetch<Player>(`/api/players/${id}`);
}

export function getPlayerStats(id: number): Promise<PlayerStat[]> {
  return apiFetch<PlayerStat[]>(`/api/players/${id}/stats`);
}
