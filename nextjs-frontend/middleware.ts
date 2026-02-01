/**
 * Next.js Middleware - Route protection and authentication.
 *
 * This middleware runs before every request to:
 * - Protect authenticated routes
 * - Redirect unauthenticated users to login
 * - Handle API route authentication
 */

import { NextRequest, NextResponse } from "next/server";

/**
 * Paths that require authentication.
 */
const protectedPaths = ["/dashboard", "/bots", "/settings"];

/**
 * Paths that should redirect authenticated users.
 */
const authPaths = ["/login", "/register"];

/**
 * Middleware handler.
 *
 * Checks for authentication token in cookies or sessionStorage
 * and redirects users based on auth state.
 */
export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Get auth token from cookie (set by token-storage.ts)
  const accessToken = request.cookies.get("auth_access_token")?.value;
  const isAuthenticated = !!accessToken;

  // Check if path requires authentication
  const isProtectedPath = protectedPaths.some((path) =>
    pathname.startsWith(path),
  );
  const isAuthPath = authPaths.some((path) => pathname.startsWith(path));

  // Redirect unauthenticated users from protected paths to login
  if (isProtectedPath && !isAuthenticated) {
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("redirect", pathname);
    return NextResponse.redirect(loginUrl);
  }

  // Redirect authenticated users from auth paths to dashboard
  if (isAuthPath && isAuthenticated) {
    const dashboardUrl = new URL("/dashboard", request.url);
    return NextResponse.redirect(dashboardUrl);
  }

  return NextResponse.next();
}

/**
 * Configuration for which paths the middleware should run on.
 */
export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - api routes that handle their own auth
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public files (images, etc.)
     */
    "/((?!api/auth|_next/static|_next/image|favicon.ico|.*\\..*).*)",
  ],
};
