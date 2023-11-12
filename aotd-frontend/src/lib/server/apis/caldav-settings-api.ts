import type { Cookies } from "@sveltejs/kit";
import { PrivateApi } from "./private-api";
import { API_BASE_URL } from "$env/static/private";

export class CalDavSettingsApi {
    private _privateApi: PrivateApi;

    constructor(private _cookies: Cookies) {
        this._privateApi = new PrivateApi(this._cookies);
    }

    public async head(): Promise<Response> {
        return await this._privateApi.head(`${API_BASE_URL}/workshop/caldav-settings/me/`);
    }

    public async get(): Promise<CalDavSettings> {
        return (await this._privateApi.get(`${API_BASE_URL}/workshop/caldav-settings/me/`) as CalDavSettings);
    }

    public async create(settings: CalDavSettings): Promise<CalDavSettings> {
        return (await this._privateApi.post(`${API_BASE_URL}/workshop/caldav-settings/me/`, settings) as CalDavSettings);
    }

    public async update(settings: CalDavSettings): Promise<CalDavSettings> {
        return (await this._privateApi.put(`${API_BASE_URL}/workshop/caldav-settings/me/`, settings) as CalDavSettings);
    }

    public async delete(): Promise<void> {
        await this._privateApi.delete(`${API_BASE_URL}/workshop/caldav-settings/me/`);
    }
}