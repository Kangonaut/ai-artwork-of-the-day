import type { Cookies } from "@sveltejs/kit";
import { PrivateApi } from "./private-api";
import { API_BASE_URL } from "$env/static/private";

export class PrivateArtworkApi {
    private _privateApi: PrivateApi;

    constructor(private _cookies: Cookies) {
        this._privateApi = new PrivateApi(this._cookies);
    }

    public async getArtworks(): Promise<Artwork[]> {
        const artworks = (await this._privateApi.get(`${API_BASE_URL}/workshop/artworks/me/`)) as Artwork[];
        return artworks;
    }
}