import { API_BASE_URL } from "$env/static/private";
import { redirect, type Cookies, error, fail, ActionFailure } from "@sveltejs/kit";
import { AuthCookies } from "$lib/cookies/auth-cookies";
import { UserCookies } from "$lib/cookies/user-cookies";

export class AuthApi {
    private static readonly _API_URL: string = `${API_BASE_URL}/auth`;

    private _authCookies: AuthCookies;
    private _userCookies: UserCookies;

    constructor(private _cookies: Cookies) {
        this._authCookies = new AuthCookies(this._cookies);
        this._userCookies = new UserCookies(this._cookies);
    }

    public async login(username: string, password: string): Promise<ActionFailure<{ error: string }>> {
        // make request
        const requestBody = {
            username,
            password
        };
        const response = await fetch(`${AuthApi._API_URL}/jwt/create/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(requestBody),
        });

        //handle response
        const responseData: object = await response.json();
        if (response.ok) {
            const loginResponse = responseData as LoginResponse;

            // set auth cookies
            this._authCookies.refreshToken = loginResponse.refresh;
            this._authCookies.accessToken = loginResponse.access;

            // redirect to root
            throw redirect(302, "/");
        }
        else {
            const errorReponse: ErrorResponse = (responseData as ErrorResponse);
            return fail(response.status, {
                error: errorReponse.detail,
            });
        }
    }

    public async logout(): Promise<never> {
        // clear auth and user related cookies
        await this._authCookies.clearCookies();
        await this._userCookies.clearCookies();

        // redirect to root
        throw redirect(302, "/");
    }

    public async refresh(): Promise<void> {
        // check if refreshToken cookie has expired
        const refreshToken = this._authCookies.refreshToken;
        if (!refreshToken) {
            console.info("refreshToken cookie expired -> redirect to login");
            throw redirect(302, "/auth/login"); // redirect to login page
        }

        // make refresh request
        const requestBody = {
            refresh: refreshToken,
        };
        const response = await fetch(`${AuthApi._API_URL}/jwt/refresh/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(requestBody),
        });

        // handle response
        const responseData = await response.json();
        if (response.ok) {
            const refreshResponse: RefreshResponse = responseData as RefreshResponse;
            this._authCookies.accessToken = refreshResponse.access;
        } else {
            const errorReponse: ErrorResponse = (responseData as ErrorResponse);
            throw error(response.status, {
                message: errorReponse.detail,
            });
        }
    }

    // public async getUserData(): Promise<UserData | undefined> {
    //     const response = await this._privateApi.get(`${AuthApi._API_URL}/users/me/`);

    //     if (response.ok)
    //         return (await response.json()) as UserData;
    //     else
    //         return undefined;
    // }
}