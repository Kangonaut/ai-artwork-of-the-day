import type { Cookies } from "@sveltejs/kit";
import { PrivateApi } from "./private-api";
import { API_BASE_URL } from "$env/static/private";
import type { Artwork } from "$lib/types/artwork";

export class PrivateArtworkApi {
    private readonly _ARTWORK_PAGE_SIZE: number = 9;

    private _privateApi: PrivateApi;

    constructor(private _cookies: Cookies) {
        this._privateApi = new PrivateApi(this._cookies);
    }

    public async getArtworksPage(page: number): Promise<Artwork[]> {
        // pagination
        const limit = this._ARTWORK_PAGE_SIZE;
        const offset = limit * page;

        const pageResponse = (await this._privateApi.get(`${API_BASE_URL}/workshop/artworks/me?limit=${limit}&offset=${offset}`)) as PageResponse;
        return pageResponse;
    }

    public async getArtworkImage(id: number): Promise<Blob> {
        const image = (await this._privateApi.getImage(`${API_BASE_URL}/workshop/artworks/${id}/image`));
        return image;
    }
}