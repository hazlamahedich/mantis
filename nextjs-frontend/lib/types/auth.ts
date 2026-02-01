/**
 * TypeScript interfaces for Keycloak JWT tokens and authentication.
 *
 * These interfaces define the shape of JWT tokens returned by Keycloak,
 * including custom claims like tenant_id for multi-tenancy support.
 */

/**
 * Keycloak JWT token claims.
 *
 * This represents the decoded JWT payload from Keycloak, including
 * both standard OIDC claims and custom claims like tenant_id.
 */
export interface KeycloakJwtClaims {
  /** Subject - User ID (UUID) */
  sub: string;

  /** Issuer - Keycloak realm URL */
  iss: string;

  /** Audience - Client ID (mantis-frontend) */
  aud: string;

  /** Expiration time - Unix timestamp */
  exp: number;

  /** Issued at time - Unix timestamp */
  iat: number;

  /** JWT ID - Unique identifier for this token */
  jti: string;

  /** Issued at time - Unix timestamp (alternate) */
  auth_time: number;

  /** Session state - Whether the session is valid */
  session_state: string;

  /** Email address */
  email: string;

  /** Email verified status */
  email_verified: boolean;

  /** Preferred username */
  preferred_username: string;

  /** Tenant ID - Custom claim for multi-tenancy */
  tenant_id: string;

  /** Given name */
  given_name?: string;

  /** Family name */
  family_name?: string;

  /** Name - Full name if available */
  name?: string;
}

/**
 * Token response from Keycloak token endpoint.
 *
 * This is the response structure when exchanging an authorization code
 * for access tokens.
 */
export interface KeycloakTokenResponse {
  /** Access token for API calls */
  access_token: string;

  /** Token type - always "Bearer" */
  token_type: string;

  /** Refresh token for obtaining new access tokens */
  refresh_token: string;

  /** ID token - JWT containing user claims */
  id_token: string;

  /** Token lifetime in seconds */
  expires_in: number;

  /** Scope granted to the token (optional) */
  scope?: string;

  /** Session state if maintaining session (optional) */
  session_state?: string;
}

/**
 * User information extracted from Keycloak token.
 *
 * This represents the user object synced to the local database.
 */
export interface KeycloakUser {
  /** User ID (UUID from Keycloak) */
  id: string;

  /** User email address */
  email: string;

  /** Email verified status */
  email_verified: boolean;

  /** Tenant ID for multi-tenancy */
  tenant_id: string;

  /** Full display name */
  name?: string;

  /** Given name */
  given_name?: string;

  /** Family name */
  family_name?: string;

  /** Account is active */
  is_active: boolean;

  /** User is verified */
  is_verified: boolean;

  /** User is superuser */
  is_superuser: boolean;
}

/**
 * Authentication state for the AuthProvider context.
 */
export interface AuthState {
  /** Whether user is authenticated */
  isAuthenticated: boolean;

  /** Whether authentication is loading */
  isLoading: boolean;

  /** Current user object if authenticated */
  user: KeycloakUser | null;

  /** Access token for API calls */
  accessToken: string | null;

  /** Refresh token for token renewal */
  refreshToken: string | null;

  /** ID token containing user claims */
  idToken: string | null;

  /** Tenant ID extracted from token */
  tenantId: string | null;

  /** Authentication error if any */
  error: string | null;
}

/**
 * Authentication context value.
 * Note: refreshToken is a function name here, not the token string.
 */
export interface AuthContextValue extends Omit<AuthState, 'refreshToken'> {
  /** Refresh token string (from AuthState) */
  refreshTokenStr: string | null;

  /** Login function - redirects to Keycloak login */
  login: (redirectUri?: string) => void;

  /** Logout function - clears session and redirects to Keycloak logout */
  logout: (redirectUri?: string) => Promise<void>;

  /** Refresh access token */
  refreshToken: () => Promise<void>;

  /** Clear authentication state */
  clearAuth: () => void;
}
