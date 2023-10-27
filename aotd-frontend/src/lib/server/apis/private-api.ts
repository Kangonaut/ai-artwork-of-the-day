import { error, type Cookies, redirect } from "@sveltejs/kit";
import { AuthCookies } from "$lib/server/cookies/auth-cookies";
import { AuthApi } from "./auth-api";

export class PrivateApi {
    private _authCookies: AuthCookies;
    private _authApi: AuthApi;

    constructor(private _cookies: Cookies) {
        this._authCookies = new AuthCookies(this._cookies);
        this._authApi = new AuthApi(this._cookies);
    }

    private async _fetch(url: string, init: RequestInit): Promise<never | object> {
        // check if accessToken cookie expired
        let accessToken = this._authCookies.accessToken;
        if (!accessToken) {
            // perform refresh
            await this._authApi.refresh();

            // acquire new access token
            accessToken = this._authCookies.accessToken;
        }

        // set headers
        init.headers = {
            "Authorization": `JWT ${accessToken}`,
            "Content-Type": "application/json",
        };

        // make request
        const response = await fetch(url, init);

        // handle response
        const responseData = await response.json();
        if (response.ok)
            return responseData;
        else if (response.status === 401) {
            console.warn(`unauthorized error: ${JSON.stringify(responseData)}`);

            // logout to invalidate session
            await this._authApi.logout();

            console.error("this should never happen!");
            throw new Error("this should never happen!"); // to shut up type checking
        } else {
            const errorResponse = responseData as ErrorResponse;
            throw error(response.status, {
                message: errorResponse.detail,
            });
        }
    }

    public async get(url: string): Promise<object> {
        return await this._fetch(url, {
            method: "GET",
        });
    }

    public async getImage(url: string): Promise<Blob> {
        let accessToken = this._authCookies.accessToken;
        if (!accessToken) {
            // perform refresh
            await this._authApi.refresh();

            // acquire new access token
            accessToken = this._authCookies.accessToken;
        }

        const init: RequestInit = {};

        // set headers
        init.headers = {
            "Authorization": `JWT ${accessToken}`,
            "Content-Type": "application/json",
        };

        // make request
        const response: Response = await fetch(url, init);

        return response.blob();
    }

    public async post(url: string, body: object): Promise<object> {
        return await this._fetch(url, {
            method: "POST",
            body: JSON.stringify(body),
        });
    }

    public async put(url: string, body: object): Promise<object> {
        return await this._fetch(url, {
            method: "PUT",
            body: JSON.stringify(body),
        });
    }

    public async delete(url: string): Promise<object> {
        return await this._fetch(url, {
            method: "DELETE",
        });
    }
}