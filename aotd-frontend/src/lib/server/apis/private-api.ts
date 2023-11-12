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

    private async _getAccessToken(): Promise<string> {
        // check if accessToken cookie expired
        let accessToken = this._authCookies.accessToken;
        if (!accessToken) {
            // perform refresh
            await this._authApi.refresh();

            // acquire new access token
            accessToken = this._authCookies.accessToken!;
        }
        return accessToken;
    }

    private _getHeaders(accessToken: string): HeadersInit {
        return {
            "Authorization": `JWT ${accessToken}`,
            "Content-Type": "application/json",
        };
    }

    private async handleResponse(response: Response): Promise<Response | never> {
        if (response.ok)
            return response;
        else {
            const responseData = await response.json();
            if (response.status === 401) {
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
    }

    private async _fetch(url: string, init: RequestInit): Promise<never | object> {
        // get access token
        const accessToken = await this._getAccessToken();

        // set headers
        init.headers = this._getHeaders(accessToken);

        // make request
        let response = await fetch(url, init);

        // handle response
        response = await this.handleResponse(response);

        // return result
        return await response.json();
    }

    public async get(url: string): Promise<object> {
        return await this._fetch(url, {
            method: "GET",
        });
    }

    public async getImage(url: string): Promise<Blob> {
        // get access token
        const accessToken = await this._getAccessToken();

        // set method
        const init: RequestInit = {
            method: "GET",
        };

        // set headers
        init.headers = this._getHeaders(accessToken);

        // make request
        let response: Response = await fetch(url, init);

        // handle response
        response = await this.handleResponse(response);

        // return result
        return await response.blob();
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

    public async delete(url: string): Promise<void> {
        // get access token
        const accessToken = await this._getAccessToken();

        // set method
        const init: RequestInit = {
            method: "DELETE",
        };

        // set headers
        init.headers = this._getHeaders(accessToken);

        // make request
        let response = await fetch(url, init);

        // handle response
        await this.handleResponse(response);
    }
}