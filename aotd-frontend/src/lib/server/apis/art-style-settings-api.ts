import type { Cookies } from "@sveltejs/kit";
import { PrivateApi } from "./private-api";
import { API_BASE_URL } from "$env/static/private";

export class ArtstyleSettingsApi {
    private _privateApi: PrivateApi;

    constructor(private _cookies: Cookies) {
        this._privateApi = new PrivateApi(this._cookies);
    }

    public async getAvailableArtstyles(): Promise<ArtStyle[]> {
        return (await this._privateApi.get(`${API_BASE_URL}/workshop/art-styles/`) as ArtStyle[]);
    }


    public async get(): Promise<ArtStyleSettings> {
        return (await this._privateApi.get(`${API_BASE_URL}/workshop/art-style-settings/me/`) as ArtStyleSettings);
    }

    public async update(settings: ArtStyleSettings): Promise<ArtStyleSettings> {
        return (await this._privateApi.put(`${API_BASE_URL}/workshop/art-style-settings/me/`, settings) as ArtStyleSettings);
    }
}