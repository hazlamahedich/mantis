import { NextRequest, NextResponse } from "next/server";
import { keycloakConfig } from "@/lib/keycloak";

export async function GET(request: NextRequest) {
    const idToken = request.cookies.get("auth_id_token")?.value;

    const params = new URLSearchParams({
        client_id: keycloakConfig.clientId,
        post_logout_redirect_uri: keycloakConfig.frontendUrl,
    });

    if (idToken) {
        params.append("id_token_hint", idToken);
    }

    const url = `${keycloakConfig.url}/realms/${keycloakConfig.realm}/protocol/openid-connect/logout?${params}`;

    const response = NextResponse.redirect(url);

    // Clear all auth cookies
    response.cookies.delete("auth_access_token");
    response.cookies.delete("auth_refresh_token");
    response.cookies.delete("auth_id_token");
    response.cookies.delete("pkce_verifier");

    return response;
}
