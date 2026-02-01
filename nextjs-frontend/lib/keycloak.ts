/**
 * Keycloak configuration for the Mantis application.
 */
export const keycloakConfig = {
    realm: process.env.NEXT_PUBLIC_KEYCLOAK_REALM || "mantis",
    clientId: "mantis-frontend",
    url: process.env.NEXT_PUBLIC_KEYCLOAK_URL || "http://localhost:8081",
    frontendUrl: process.env.NEXT_PUBLIC_FRONTEND_URL || "http://localhost:3000",
} as const;
