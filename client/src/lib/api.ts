import { getAccessToken, refreshAccessToken } from "@/lib/auth";

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message);
  }
}

export async function apiFetch<T>(
  path: string,
  init?: RequestInit,
): Promise<T> {
  const makeRequest = async (token: string | null): Promise<Response> => {
    const headers = new Headers(init?.headers);

    if (init?.body && !headers.has("Content-Type")) {
      headers.set("Content-Type", "application/json");
    }
    if (token) {
      headers.set("Authorization", `Bearer ${token}`);
    }

    return fetch(`${API_BASE}${path}`, {
      ...init,
      headers,
      credentials: "include",
    });
  };

  let res = await makeRequest(getAccessToken());

  if (res.status === 401 && path !== "/api/auth/refresh") {
    const refreshedToken = await refreshAccessToken();
    if (refreshedToken) {
      res = await makeRequest(refreshedToken);
    }
  }

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new ApiError(res.status, body.detail ?? `API error ${res.status}`);
  }

  if (res.status === 204) return undefined as T;
  return res.json() as Promise<T>;
}
