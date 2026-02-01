import { NextRequest, NextResponse } from "next/server";

export async function GET(request: NextRequest) {
    const accessToken = request.cookies.get("auth_access_token")?.value;
    const idToken = request.cookies.get("auth_id_token")?.value;

    if (!accessToken || !idToken) {
        return NextResponse.json({ isAuthenticated: false });
    }

    try {
        // Decode ID token to get user info (no verification needed here as cookie is secure)
        // Verification happens on backend requests using the access token
        const parts = idToken.split(".");
        if (parts.length !== 3) throw new Error("Invalid JWT");

        const payload = JSON.parse(Buffer.from(parts[1], "base64").toString());

        return NextResponse.json({
            isAuthenticated: true,
            user: {
                id: payload.sub,
                email: payload.email,
                email_verified: payload.email_verified,
                tenant_id: payload.tenant_id,
                name: payload.name,
                given_name: payload.given_name,
                family_name: payload.family_name,
                is_active: true,
                is_verified: payload.email_verified,
                is_superuser: false,
            },
        });
    } catch (error) {
        return NextResponse.json({ isAuthenticated: false });
    }
}
