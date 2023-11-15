import type { Cookies } from "@sveltejs/kit";
import { PrivateApi } from "./private-api";
import { API_BASE_URL } from "$env/static/private";

export class UserSettingsApi {
    private _privateApi: PrivateApi;

    constructor(private _cookies: Cookies) {
        this._privateApi = new PrivateApi(this._cookies);
    }

    public async head(): Promise<Response> {
        return await this._privateApi.head(`${API_BASE_URL}/workshop/user-settings/me/`);
    }

    public async get(): Promise<UserSettings> {
        return (await this._privateApi.get(`${API_BASE_URL}/workshop/user-settings/me/`) as UserSettings);
    }

    public async create(settings: UserSettings): Promise<UserSettings> {
        return (await this._privateApi.post(`${API_BASE_URL}/workshop/user-settings/me/`, settings) as UserSettings);
    }

    public async update(settings: UserSettings): Promise<UserSettings> {
        return (await this._privateApi.put(`${API_BASE_URL}/workshop/user-settings/me/`, settings) as UserSettings);
    }

    public async delete(): Promise<void> {
        await this._privateApi.delete(`${API_BASE_URL}/workshop/user-settings/me/`);
    }
}