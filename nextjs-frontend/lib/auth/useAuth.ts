/**
 * useAuth hook - Re-export from AuthProvider for convenience.
 *
 * This hook provides access to the authentication context.
 * Use this in components to check auth state, login, logout, etc.
 */

export { useAuth } from "@/components/providers/AuthProvider";
export type { AuthContextValue, AuthState, KeycloakUser, KeycloakJwtClaims } from "@/lib/types/auth";
