import { error, type Cookies } from "@sveltejs/kit";
import { AuthCookies } from "$lib/cookies/auth-cookies";

export class PrivateApi {
    private _authCookies: AuthCookies;

    constructor(private _cookies: Cookies) {
        this._authCookies = new AuthCookies(this._cookies);
    }

    private async _fetch(url: string, init: RequestInit): Promise<object> {
        // check if accessToken cookie expired
        const accessToken = this._authCookies.accessToken;
        if (!accessToken) {
            // TODO: implement refresh
            throw new AccessTokenExpiredApiError();
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
        else {
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