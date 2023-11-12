import type { Cookies } from "@sveltejs/kit";
import { PrivateApi } from "./private-api";
import { API_BASE_URL } from "$env/static/private";

export class DaytimeSettingsApi {
    private _privateApi: PrivateApi;

    constructor(private _cookies: Cookies) {
        this._privateApi = new PrivateApi(this._cookies);
    }

    public async get(): Promise<DaytimeSettings> {
        return (await this._privateApi.get(`${API_BASE_URL}/workshop/daytime-settings/me/`) as DaytimeSettings);
    }

    public async create(settings: DaytimeSettings): Promise<DaytimeSettings> {
        return (await this._privateApi.post(`${API_BASE_URL}/workshop/daytime-settings/me/`, settings) as DaytimeSettings);
    }

    public async update(settings: DaytimeSettings): Promise<DaytimeSettings> {
        return (await this._privateApi.put(`${API_BASE_URL}/workshop/daytime-settings/me/`, settings) as DaytimeSettings);
    }

    public async delete(): Promise<void> {
        await this._privateApi.delete(`${API_BASE_URL}/workshop/daytime-settings/me/`);
    }
}