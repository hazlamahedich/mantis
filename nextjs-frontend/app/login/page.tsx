/**
 * Login Page - Redirects to Keycloak for authentication.
 */

"use client";

import { useEffect, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useAuth } from "@/components/providers/AuthProvider";

function LoginForm() {
  const { user, login, isAuthenticated } = useAuth();
  const router = useRouter();
  const searchParams = useSearchParams();

  useEffect(() => {
    if (isAuthenticated) {
      router.push("/dashboard");
      return;
    }

    const error = searchParams.get("error");
    if (error) {
      console.error("Login error:", error);
    }

    // Automatically trigger Keycloak login
    login();
  }, [isAuthenticated, router, login, searchParams]);

  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="text-center">
        <h2 className="text-2xl font-bold mb-4">Redirecting to Login</h2>
        <p className="text-gray-600">Please wait while we redirect you to the authentication provider.</p>
        <div className="mt-8">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto"></div>
        </div>
      </div>
    </div>
  );
}

export default function Page() {
  return (
    <Suspense fallback={<div>Loading login...</div>}>
      <LoginForm />
    </Suspense>
  );
}
