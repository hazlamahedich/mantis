/**
 * Register Page - Placeholder for registration.
 *
 * In this setup, registration is handled by Keycloak.
 */

"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";

export default function RegisterPage() {
  const router = useRouter();

  const handleKeycloakRegister = () => {
    // We can redirect to login, Keycloak usually has a register link.
    // Or we can construct a specific register URL if we know the endpoint.
    // For simplicity, redirect to login which initiates the flow.
    window.location.href = "/api/auth/login";
  };

  return (
    <div className="flex min-h-screen items-center justify-center">
      <p>Redirecting to registration...</p>
    </div>
  );
}
