import type { UserData } from "$lib/server/types/user";
import type { Cookies } from "@sveltejs/kit";
import { AuthApi } from "./auth-api";
import { UserCookies } from "$lib/server/cookies/user-cookies";
import { PrivateApi } from "./private-api";
import { API_BASE_URL } from "$env/static/private";

export class UserApi {
    private _privateApi: PrivateApi;
    private _userCookies: UserCookies;

    constructor(private _cookies: Cookies) {
        this._privateApi = new PrivateApi(_cookies);
        this._userCookies = new UserCookies(this._cookies);
    }

    private async updateUserDataFromServer(): Promise<UserData> {
        const userData = await this._privateApi.get(`${API_BASE_URL}/auth/users/me/`) as UserData;
        this._userCookies.userData = userData;
        return userData;
    }

    public async getUserData(): Promise<UserData> {
        // check if cookie is set
        const userData = this._userCookies.userData;
        if (userData)
            return userData;

        // if cookie not set -> fetch from server
        return await this.updateUserDataFromServer();
    }
}