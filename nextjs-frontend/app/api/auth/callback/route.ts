import { NextRequest, NextResponse } from "next/server";
import { keycloakConfig } from "@/lib/keycloak";

export async function GET(request: NextRequest) {
    const searchParams = request.nextUrl.searchParams;
    const code = searchParams.get("code");
    const state = searchParams.get("state");
    const error = searchParams.get("error");

    if (error) {
        return NextResponse.redirect(new URL(`/?error=${error}`, request.url));
    }

    if (!code) {
        return NextResponse.redirect(new URL("/?error=no_code", request.url));
    }

    // Retrieve code verifier from cookie
    const codeVerifier = request.cookies.get("pkce_verifier")?.value;

    if (!codeVerifier) {
        return NextResponse.redirect(new URL("/?error=no_verifier", request.url));
    }

    // Exchange code for tokens
    try {
        const tokenUrl = `${keycloakConfig.url}/realms/${keycloakConfig.realm}/protocol/openid-connect/token`;

        const tokenResponse = await fetch(tokenUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: new URLSearchParams({
                grant_type: "authorization_code",
                client_id: keycloakConfig.clientId,
                code: code,
                redirect_uri: `${keycloakConfig.frontendUrl}/api/auth/callback`,
                code_verifier: codeVerifier,
            }),
        });

        if (!tokenResponse.ok) {
            const text = await tokenResponse.text();
            console.error("Token exchange failed:", text);
            return NextResponse.redirect(new URL("/?error=token_exchange_failed", request.url));
        }

        const tokens = await tokenResponse.json();

        // Determine redirect destination from state
        let redirectPath = "/dashboard";
        try {
            if (state) {
                const stateData = JSON.parse(decodeURIComponent(state));
                if (stateData.redirect) {
                    redirectPath = stateData.redirect;
                }
            }
        } catch (e) {
            // Ignore JSON parse error, use default
        }

        const response = NextResponse.redirect(new URL(redirectPath, request.url));

        // Clear verifier cookie
        response.cookies.delete("pkce_verifier");

        // Set token cookies
        const cookieOptions = {
            httpOnly: true,
            secure: process.env.NODE_ENV === "production",
            sameSite: "lax" as const,
            path: "/",
        };

        response.cookies.set("auth_access_token", tokens.access_token, {
            ...cookieOptions,
            maxAge: tokens.expires_in,
        });

        response.cookies.set("auth_refresh_token", tokens.refresh_token, {
            ...cookieOptions,
            maxAge: tokens.refresh_expires_in || 7 * 24 * 60 * 60,
        });

        response.cookies.set("auth_id_token", tokens.id_token, {
            ...cookieOptions,
            maxAge: tokens.expires_in,
        });

        return response;

    } catch (e) {
        console.error("Callback error:", e);
        return NextResponse.redirect(new URL("/?error=callback_exception", request.url));
    }
}
