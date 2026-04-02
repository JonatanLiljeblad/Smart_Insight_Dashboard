"use client";

import { useCallback, useEffect, useState } from "react";
import type { Favorite } from "@/types/favorite";
import * as favoriteService from "@/services/favorite-service";

export function useFavorites() {
  const [favorites, setFavorites] = useState<Favorite[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await favoriteService.getFavorites();
      setFavorites(data);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to load favorites",
      );
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const addFavorite = useCallback(
    async (playerId: number) => {
      await favoriteService.addFavorite(playerId);
      await refresh();
    },
    [refresh],
  );

  const removeFavorite = useCallback(
    async (favoriteId: number) => {
      await favoriteService.removeFavorite(favoriteId);
      await refresh();
    },
    [refresh],
  );

  return { favorites, isLoading, error, addFavorite, removeFavorite, refresh };
}
