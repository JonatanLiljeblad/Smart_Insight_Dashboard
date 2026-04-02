"use client";

import Link from "next/link";
import type { Player } from "@/types/player";

interface PlayerTableProps {
  players: Player[];
  isLoading: boolean;
}

export default function PlayerTable({ players, isLoading }: PlayerTableProps) {
  if (isLoading) {
    return (
      <div className="rounded-xl border border-gray-200 bg-white p-8 text-center text-sm text-gray-500">
        Loading players…
      </div>
    );
  }

  if (players.length === 0) {
    return (
      <div className="rounded-xl border border-gray-200 bg-white p-8 text-center">
        <p className="text-sm text-gray-500">
          No players yet. Seed data to see them here.
        </p>
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm">
      <table className="w-full text-left text-sm">
        <thead className="border-b border-gray-100 bg-gray-50">
          <tr>
            <th className="px-6 py-3 font-medium text-gray-500">Name</th>
            <th className="px-6 py-3 font-medium text-gray-500">
              Nationality
            </th>
            <th className="px-6 py-3 font-medium text-gray-500">Tour</th>
            <th className="px-6 py-3 font-medium text-gray-500" />
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100">
          {players.map((player) => (
            <tr key={player.id} className="hover:bg-gray-50">
              <td className="px-6 py-4 font-medium text-gray-900">
                {player.name}
              </td>
              <td className="px-6 py-4 text-gray-600">
                {player.nationality ?? "—"}
              </td>
              <td className="px-6 py-4 text-gray-600">
                {player.tour ?? "—"}
              </td>
              <td className="px-6 py-4 text-right">
                <Link
                  href={`/players/${player.id}`}
                  className="text-sm font-medium text-blue-600 hover:text-blue-500"
                >
                  View
                </Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
