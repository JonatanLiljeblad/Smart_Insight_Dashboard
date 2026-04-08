export interface PredictionJob {
  id: number;
  player_id: number;
  status: "pending" | "running" | "completed" | "failed";
  result: {
    predicted_scoring_average: number;
    features_used: Record<string, number>;
    model: string;
  } | null;
  error_message: string | null;
  created_at: string;
  completed_at: string | null;
}
