import { BASE_API_URL } from "$env/static/private";
import { PrivateApi } from "./private-api";
import type { Cookies } from "@sveltejs/kit";
import type { UserData } from "$lib/types/user";

interface LoginResponse {
    refresh: string;
    access: string;
}

interface ErrorResponse {
    detail: string;
}

export class AuthApi {
    private static readonly _API_URL: string = `${BASE_API_URL}/auth`;

    private _privateApi: PrivateApi;

    constructor(private _cookies: Cookies) {
        this._privateApi = new PrivateApi(this._cookies);
    }

    public static async login(username: string, password: string): Promise<LoginResponse> {
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

        const responseData: object = await response.json();

        if (response.ok)
            return responseData as LoginResponse;
        else
            throw new Error((responseData as ErrorResponse).detail);
    }

    public async getUserData(): Promise<UserData | undefined> {
        const response = await this._privateApi.get(`${AuthApi._API_URL}/users/me/`);

        if (response.ok)
            return (await response.json()) as UserData;
        else
            return undefined;
    }
}