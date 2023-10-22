import { AuthApi } from "$lib/apis/auth-api";
import type { UserData } from "$lib/types/user";
import type { Cookies } from "@sveltejs/kit";

export class AuthManager {
    private _authApi: AuthApi;

    constructor(private _cookies: Cookies) { 
        this._authApi = new AuthApi(this._cookies);
    }

    public async getUserData(): Promise<UserData> {
        // only fetch api if cookie is not set
        const userData = await this._authApi.getUserData();

        if (userData)
            return userData;
        else {
            // TODO: check if accessToken is still valid and refresh if not
            return {
                id: -1,
                username: "Nobody",
            };
        }
    }
}