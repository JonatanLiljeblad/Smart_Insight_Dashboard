"use client";

import { useCallback, useEffect, useState } from "react";
import type { Player, PlayerStat } from "@/types/player";
import { getPlayers, getPlayer, getPlayerStats } from "@/services/player-service";

export function usePlayers() {
  const [players, setPlayers] = useState<Player[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await getPlayers();
      setPlayers(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load players");
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  return { players, isLoading, error, refresh };
}

export function usePlayer(id: number) {
  const [player, setPlayer] = useState<Player | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setIsLoading(true);
    getPlayer(id)
      .then(setPlayer)
      .catch((err) =>
        setError(err instanceof Error ? err.message : "Failed to load player"),
      )
      .finally(() => setIsLoading(false));
  }, [id]);

  return { player, isLoading, error };
}

export function usePlayerStats(id: number) {
  const [stats, setStats] = useState<PlayerStat[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setIsLoading(true);
    getPlayerStats(id)
      .then(setStats)
      .catch(() => setStats([]))
      .finally(() => setIsLoading(false));
  }, [id]);

  return { stats, isLoading };
}
