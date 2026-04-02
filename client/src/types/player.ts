export interface Player {
  id: number;
  external_id: string;
  name: string;
  nationality: string | null;
  tour: string | null;
  created_at: string;
}

export interface PlayerStat {
  id: number;
  player_id: number;
  event_date: string;
  scoring_average: number | null;
  strokes_gained_total: number | null;
  driving_accuracy: number | null;
  greens_in_regulation: number | null;
  putting_average: number | null;
  created_at: string;
}
