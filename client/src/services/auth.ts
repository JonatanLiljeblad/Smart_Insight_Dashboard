import { apiFetch } from "@/lib/api";
import type { User, Token } from "@/types/user";

export async function signup(username: string, email: string, password: string): Promise<User> {
  return apiFetch<User>("/api/auth/signup", {
    method: "POST",
    body: JSON.stringify({ username, email, password }),
  });
}

export async function login(email: string, password: string): Promise<Token> {
  return apiFetch<Token>("/api/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}
