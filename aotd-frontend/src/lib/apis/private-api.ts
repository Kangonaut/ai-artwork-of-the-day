import type { Cookies } from "@sveltejs/kit";
import { AuthCookies } from "$lib/cookies/auth-cookies";
import { AccessTokenExpiredError, UnauthorizedApiError, UnexpectedApiError } from "$lib/types/errors";

export class PrivateApi {
    private _authCookies: AuthCookies;

    constructor(private _cookies: Cookies) {
        this._authCookies = new AuthCookies(this._cookies);
    }

    private async _fetch(url: string, init: RequestInit): Promise<Response> {
        // check if accessToken cookie expired
        const accessToken = this._authCookies.accessToken;
        if (!accessToken) {
            // TODO: implement refresh
            throw new AccessTokenExpiredError();
        }

        // set headers
        init.headers = {
            "Authorization": `JWT ${accessToken}`,
            "Content-Type": "application/json",
        };

        // make request
        const response = await fetch(url, init);

        // handle response
        if (response.ok)
            return response;
        else if (response.status === 401)
            throw new UnauthorizedApiError(response.statusText);
        else
            throw new UnexpectedApiError(`${response.status} - ${response.statusText}`);
    }

    public async get(url: string): Promise<Response> {
        return await this._fetch(url, {
            method: "GET",
        });
    }

    public async post(url: string, body: object): Promise<Response> {
        return await this._fetch(url, {
            method: "POST",
            body: JSON.stringify(body),
        });
    }

    public async put(url: string, body: object): Promise<Response> {
        return await this._fetch(url, {
            method: "PUT",
            body: JSON.stringify(body),
        });
    }

    public async delete(url: string): Promise<Response> {
        return await this._fetch(url, {
            method: "DELETE",
        });
    }
}