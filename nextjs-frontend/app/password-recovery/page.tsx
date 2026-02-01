/**
 * Password Recovery Page - Placeholder.
 *
 * In this setup, password recovery is handled by Keycloak.
 */

"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function PasswordRecoveryPage() {
  const router = useRouter();

  useEffect(() => {
    // Redirect to login, where Keycloak can handle password recovery
    router.push("/login?action=forgot_password");
  }, [router]);

  return (
    <div className="flex min-h-screen items-center justify-center">
      <p>Redirecting to password recovery...</p>
    </div>
  );
}
