import type { Cookies } from "@sveltejs/kit";
import { PrivateApi } from "./private-api";
import { API_BASE_URL } from "$env/static/private";

export class WeatherSettingsApi {
    private _privateApi: PrivateApi;

    constructor(private _cookies: Cookies) {
        this._privateApi = new PrivateApi(this._cookies);
    }

    public async head(): Promise<Response> {
        return await this._privateApi.head(`${API_BASE_URL}/workshop/open-weather-settings/me/`);
    }

    public async get(): Promise<WeatherSettings> {
        return (await this._privateApi.get(`${API_BASE_URL}/workshop/open-weather-settings/me/`) as WeatherSettings);
    }

    public async create(settings: WeatherSettings): Promise<WeatherSettings> {
        return (await this._privateApi.post(`${API_BASE_URL}/workshop/open-weather-settings/me/`, settings) as WeatherSettings);
    }

    public async update(settings: WeatherSettings): Promise<WeatherSettings> {
        return (await this._privateApi.put(`${API_BASE_URL}/workshop/open-weather-settings/me/`, settings) as WeatherSettings);
    }

    public async delete(): Promise<void> {
        await this._privateApi.delete(`${API_BASE_URL}/workshop/open-weather-settings/me/`);
    }
}