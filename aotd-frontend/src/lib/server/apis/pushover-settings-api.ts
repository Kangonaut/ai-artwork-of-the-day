import type { Cookies } from "@sveltejs/kit";
import { PrivateApi } from "./private-api";
import { API_BASE_URL } from "$env/static/private";

export class PushoverSettingsApi {
    private _privateApi: PrivateApi;

    constructor(private _cookies: Cookies) {
        this._privateApi = new PrivateApi(this._cookies);
    }

    public async head(): Promise<Response> {
        return await this._privateApi.head(`${API_BASE_URL}/workshop/pushover-settings/me/`);
    }

    public async get(): Promise<PushoverSettings> {
        return (await this._privateApi.get(`${API_BASE_URL}/workshop/pushover-settings/me/`) as PushoverSettings);
    }

    public async create(settings: PushoverSettings): Promise<PushoverSettings> {
        return (await this._privateApi.post(`${API_BASE_URL}/workshop/pushover-settings/me/`, settings) as PushoverSettings);
    }

    public async update(settings: PushoverSettings): Promise<PushoverSettings> {
        return (await this._privateApi.put(`${API_BASE_URL}/workshop/pushover-settings/me/`, settings) as PushoverSettings);
    }

    public async delete(): Promise<void> {
        await this._privateApi.delete(`${API_BASE_URL}/workshop/pushover-settings/me/`);
    }
}