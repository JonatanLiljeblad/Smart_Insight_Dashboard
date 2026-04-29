import { clearAccessToken, refreshAccessToken, setAccessToken } from "@/lib/auth";
import { apiFetch } from "@/lib/api";
import type { User } from "@/types/user";
import type { Token, LoginPayload, RegisterPayload } from "@/types/auth";

export function register(payload: RegisterPayload): Promise<User> {
  return apiFetch<User>("/api/auth/register", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function login(payload: LoginPayload): Promise<Token> {
  return apiFetch<Token>("/api/auth/login", {
    method: "POST",
    body: JSON.stringify(payload),
  }).then((token) => {
    setAccessToken(token.access_token);
    return token;
  });
}

export function getCurrentUser(): Promise<User> {
  return apiFetch<User>("/api/auth/me");
}

export function refresh(): Promise<string | null> {
  return refreshAccessToken();
}

export async function logout(): Promise<void> {
  await apiFetch<void>("/api/auth/logout", { method: "POST" });
  clearAccessToken();
}
