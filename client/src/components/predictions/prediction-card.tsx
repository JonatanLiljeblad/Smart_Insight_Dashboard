"use client";

import { usePrediction } from "@/hooks/usePrediction";
import Button from "@/components/ui/button";

interface PredictionCardProps {
  playerId: number;
}

export default function PredictionCard({ playerId }: PredictionCardProps) {
  const { job, isLoading, error, requestPrediction, reset } = usePrediction();

  return (
    <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold text-gray-900">
          ML Score Prediction
        </h2>
        {job?.status === "completed" && (
          <button
            onClick={reset}
            className="text-xs text-gray-400 hover:text-gray-600"
          >
            Reset
          </button>
        )}
      </div>
      <p className="mt-1 text-sm text-gray-500">
        Predict this player&apos;s expected next scoring average using recent
        performance data.
      </p>

      <div className="mt-4">
        {/* Idle state */}
        {!job && !isLoading && !error && (
          <Button onClick={() => requestPrediction(playerId)}>
            Generate Prediction
          </Button>
        )}

        {/* Loading state */}
        {isLoading && (
          <div className="flex items-center gap-3">
            <div className="h-5 w-5 animate-spin rounded-full border-2 border-blue-600 border-t-transparent" />
            <span className="text-sm text-gray-600">
              {job?.status === "pending"
                ? "Queued — waiting for worker…"
                : "Running prediction model…"}
            </span>
          </div>
        )}

        {/* Error state */}
        {error && (
          <div className="space-y-3">
            <p className="text-sm text-red-600">{error}</p>
            <Button
              variant="secondary"
              size="sm"
              onClick={() => requestPrediction(playerId)}
            >
              Retry
            </Button>
          </div>
        )}

        {/* Failed job */}
        {job?.status === "failed" && !isLoading && (
          <div className="space-y-3">
            <p className="text-sm text-red-600">
              {job.error_message || "Prediction failed"}
            </p>
            <Button
              variant="secondary"
              size="sm"
              onClick={() => requestPrediction(playerId)}
            >
              Retry
            </Button>
          </div>
        )}

        {/* Success state */}
        {job?.status === "completed" && job.result && (
          <div className="space-y-4">
            <div className="rounded-lg bg-blue-50 p-4">
              <p className="text-xs font-medium text-blue-700">
                Predicted Scoring Average
              </p>
              <p className="mt-1 text-3xl font-bold text-blue-900">
                {job.result.predicted_scoring_average.toFixed(2)}
              </p>
              <p className="mt-1 text-xs text-blue-600">
                Model: {job.result.model}
              </p>
            </div>
            <div>
              <p className="mb-2 text-xs font-medium text-gray-500">
                Features Used
              </p>
              <div className="grid grid-cols-2 gap-2 sm:grid-cols-3">
                {Object.entries(job.result.features_used).map(
                  ([key, value]) => (
                    <div
                      key={key}
                      className="rounded-md bg-gray-50 px-3 py-2 text-xs"
                    >
                      <span className="text-gray-500">
                        {key.replace(/_/g, " ")}
                      </span>
                      <span className="ml-1 font-medium text-gray-900">
                        {typeof value === "number" ? value.toFixed(2) : value}
                      </span>
                    </div>
                  )
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
