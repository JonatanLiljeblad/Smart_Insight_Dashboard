"use client";

import { useState, useRef, useCallback, useEffect } from "react";
import type { PredictionJob } from "@/types/prediction";
import { createPrediction, getPrediction } from "@/services/prediction-service";

const POLL_INTERVAL = 2000;

export function usePrediction() {
  const [job, setJob] = useState<PredictionJob | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const stopPolling = useCallback(() => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
  }, []);

  const pollJob = useCallback(
    (jobId: number) => {
      intervalRef.current = setInterval(async () => {
        try {
          const updated = await getPrediction(jobId);
          setJob(updated);
          if (updated.status === "completed" || updated.status === "failed") {
            stopPolling();
            setIsLoading(false);
          }
        } catch {
          stopPolling();
          setIsLoading(false);
          setError("Failed to check prediction status");
        }
      }, POLL_INTERVAL);
    },
    [stopPolling]
  );

  const requestPrediction = useCallback(
    async (playerId: number) => {
      stopPolling();
      setJob(null);
      setError(null);
      setIsLoading(true);

      try {
        const created = await createPrediction(playerId);
        setJob(created);
        pollJob(created.id);
      } catch {
        setIsLoading(false);
        setError("Failed to create prediction");
      }
    },
    [stopPolling, pollJob]
  );

  const reset = useCallback(() => {
    stopPolling();
    setJob(null);
    setError(null);
    setIsLoading(false);
  }, [stopPolling]);

  useEffect(() => {
    return () => stopPolling();
  }, [stopPolling]);

  return { job, isLoading, error, requestPrediction, reset };
}
