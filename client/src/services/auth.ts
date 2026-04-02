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
  });
}

export function getCurrentUser(): Promise<User> {
  return apiFetch<User>("/api/auth/me");
}
