import { NextRequest, NextResponse } from "next/server";
import { keycloakConfig } from "@/lib/keycloak";
import { generateCodeVerifier, generateCodeChallenge } from "@/lib/auth/pkce";

export async function GET(request: NextRequest) {
    const codeVerifier = generateCodeVerifier();
    const codeChallenge = generateCodeChallenge(codeVerifier);

    // Get redirect param or default
    const redirectPath = request.nextUrl.searchParams.get("redirect") || "/dashboard";

    // Build state to include redirect path
    const state = encodeURIComponent(JSON.stringify({ redirect: redirectPath }));

    const params = new URLSearchParams({
        client_id: keycloakConfig.clientId,
        redirect_uri: `${keycloakConfig.frontendUrl}/api/auth/callback`,
        response_type: "code",
        scope: "openid profile email",
        code_challenge: codeChallenge,
        code_challenge_method: "S256",
        state: state,
    });

    const url = `${keycloakConfig.url}/realms/${keycloakConfig.realm}/protocol/openid-connect/auth?${params}`;

    const response = NextResponse.redirect(url);

    // Store code verifier in cookie for callback
    response.cookies.set("pkce_verifier", codeVerifier, {
        httpOnly: true,
        secure: process.env.NODE_ENV === "production",
        sameSite: "lax",
        path: "/",
        maxAge: 300, // 5 minutes
    });

    return response;
}
