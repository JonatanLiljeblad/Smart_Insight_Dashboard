import { apiFetch } from "@/lib/api";
import type { PredictionJob } from "@/types/prediction";

export async function createPrediction(
  playerId: number
): Promise<PredictionJob> {
  return apiFetch("/api/predictions/", {
    method: "POST",
    body: JSON.stringify({ player_id: playerId }),
  });
}

export async function getPrediction(jobId: number): Promise<PredictionJob> {
  return apiFetch(`/api/predictions/${jobId}`);
}
