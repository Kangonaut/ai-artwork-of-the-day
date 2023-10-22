import { SERVER_ENV } from "$env/static/private";
import type { UserData } from "$lib/types/user";
import type { Cookies } from "@sveltejs/kit";

export class UserCookies {
    private static readonly _USER_COOKIE_MAX_AGE: number = 60 * 60 * 1; // 1 hour

    constructor(private _cookies: Cookies) { }

    private _setUserCookie(name: string, value: string) {
        this._cookies.set(name, value, {
            path: "/",  // will be sent alongsdie each request
            httpOnly: true,  // prevents the JS client from accessing the cookie
            sameSite: "strict", // cookie is only sent to the site where it originated (prevents CSRF)
            secure: SERVER_ENV == "PROD", // true = only sent when using HTTPS
            maxAge: UserCookies._USER_COOKIE_MAX_AGE,  // expire cookie 1 minute early
        });
    }

    public get userData(): UserData | undefined {
        const value: string | undefined = this._cookies.get("userData");
        if (value)
            return JSON.parse(value) as UserData;
        else
            return undefined;
    }

    public set userData(userData: UserData) {
        this._setUserCookie("userData", JSON.stringify(userData));
    }

    public async clearCookies(): Promise<void> {
        this._cookies.delete("userData", {
            path: "/",
        });
    }
}