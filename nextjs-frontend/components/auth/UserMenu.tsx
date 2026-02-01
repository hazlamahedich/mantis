/**
 * UserMenu component - Displays user avatar and logout button.
 *
 * This client component uses the useAuth hook to access user info
 * and handle logout with Keycloak.
 */

"use client";

import Link from "next/link";
import { useAuth } from "@/lib/auth/useAuth";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";

/**
 * UserMenu component.
 *
 * Shows user avatar with dropdown menu containing:
 * - User info display
 * - Support link
 * - Logout button (Keycloak)
 */
export function UserMenu() {
  const { user, logout, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center w-10 h-10 rounded-full bg-gray-300 animate-pulse" />
    );
  }

  // Get user initials for avatar fallback
  const getUserInitials = () => {
    if (!user) return "U";
    const name = user.name || user.email;
    return name
      .split(" ")
      .map((n) => n[0])
      .join("")
      .toUpperCase()
      .slice(0, 2);
  };

  return (
    <div className="relative">
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <button className="flex items-center justify-center w-10 h-10 rounded-full bg-gray-300 hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-primary">
            <Avatar>
              <AvatarFallback>{getUserInitials()}</AvatarFallback>
            </Avatar>
          </button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end" side="bottom">
          {user && (
            <div className="px-4 py-2 border-b">
              <p className="text-sm font-medium">{user.name || user.email}</p>
              <p className="text-xs text-muted-foreground">{user.email}</p>
              {user.tenant_id && (
                <p className="text-xs text-muted-foreground mt-1">
                  Tenant: {user.tenant_id}
                </p>
              )}
            </div>
          )}
          <DropdownMenuItem asChild>
            <Link
              href="/support"
              className="block cursor-pointer"
            >
              Support
            </Link>
          </DropdownMenuItem>
          <DropdownMenuItem
            onClick={() => logout()}
            className="cursor-pointer"
          >
            Logout
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  );
}
