/**
 * AuthProvider - React Context for Keycloak authentication.
 *
 * This provider manages authentication state using Server-Side Auth (BFF Pattern).
 * It fetches session state from /api/auth/session and handles login/logout redirects.
 */

"use client";

import React, { createContext, useContext, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { AuthContextValue, AuthState } from "@/lib/types/auth";

const initialAuthState: AuthState = {
  isAuthenticated: false,
  isLoading: true,
  user: null,
  accessToken: null,
  refreshToken: null,
  idToken: null,
  tenantId: null,
  error: null,
};

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

interface AuthProviderProps {
  children: React.ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const router = useRouter();
  const [authState, setAuthState] = useState<AuthState>(initialAuthState);

  /**
   * Fetch session from server (BFF).
   */
  async function checkSession() {
    try {
      const res = await fetch("/api/auth/session");
      if (res.ok) {
        const data = await res.json();
        if (data.isAuthenticated) {
          setAuthState({
            isAuthenticated: true,
            isLoading: false,
            user: data.user,
            accessToken: "http-only-cookie", // Placeholder, not accessible
            refreshToken: "http-only-cookie",
            idToken: "http-only-cookie",
            tenantId: data.user.tenant_id,
            error: null,
          });
          return;
        }
      }
      setAuthState((prev) => ({ ...prev, isAuthenticated: false, isLoading: false, user: null }));
    } catch (e) {
      console.error("Session check failed", e);
      setAuthState((prev) => ({ ...prev, isAuthenticated: false, isLoading: false, user: null }));
    }
  }

  useEffect(() => {
    checkSession();
  }, []);

  async function login(redirectUri?: string) {
    const url = new URL("/api/auth/login", window.location.href);
    if (redirectUri) {
      url.searchParams.set("redirect", redirectUri);
    }
    window.location.href = url.toString();
  }

  async function logout(redirectUri?: string) {
    window.location.href = "/api/auth/logout";
  }

  /**
   * Refresh is handled automatically by cookies but we can force a session check
   */
  async function refreshToken() {
    await checkSession();
  }

  function clearAuth() {
    setAuthState((prev) => ({ ...prev, isAuthenticated: false, user: null }));
  }

  const contextValue: AuthContextValue = {
    ...authState,
    refreshTokenStr: null,
    login,
    logout,
    refreshToken,
    clearAuth,
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
