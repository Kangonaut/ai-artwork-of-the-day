import type { Cookies } from "@sveltejs/kit";
import { SERVER_ENV } from "$env/static/private";

enum AuthTokenType {
    ACCESS = "accessToken",
    REFRESH = "refreshToken",
}

export class AuthCookies {
    private static readonly AUTH_TOKEN_MAX_AGE_MAP: Map<AuthTokenType, number> = new Map([
        [AuthTokenType.ACCESS, 60 * 60 * 24 * 1], // 1 day
        [AuthTokenType.REFRESH, 60 * 60 * 24 * 7], // 1 day
    ]);

    constructor(private cookies: Cookies) { }

    private setAuthTokenCookie(type: AuthTokenType, token: string): void {
        this.cookies.set(type.valueOf(), token, {
            path: "/",  // will be sent alongsdie each request
            httpOnly: true,  // prevents the JS client from accessing the cookie
            sameSite: "strict", // cookie is only sent to the site where it originated (prevents CSRF)
            secure: SERVER_ENV == "PROD", // true = only sent when using HTTPS
            maxAge: AuthCookies.AUTH_TOKEN_MAX_AGE_MAP.get(type)! - (60 * 1),  // expire cookie 1 minute early 
        });
    }

    public setAccessTokenCookie(accessToken: string): void {
        this.setAuthTokenCookie(AuthTokenType.ACCESS, accessToken);
    }

    public setRefreshTokenCookie(refreshToken: string): void {
        this.setAuthTokenCookie(AuthTokenType.REFRESH, refreshToken);
    }
}