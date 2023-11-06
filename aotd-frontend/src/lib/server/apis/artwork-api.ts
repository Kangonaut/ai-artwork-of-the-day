import type { Cookies } from "@sveltejs/kit";
import { PrivateApi } from "./private-api";
import { API_BASE_URL } from "$env/static/private";
import type { Artwork } from "$lib/types/artwork";

export class ArtworkApi {
    private readonly _ARTWORK_PAGE_SIZE: number = 9;

    private _privateApi: PrivateApi;

    constructor(private _cookies: Cookies) {
        this._privateApi = new PrivateApi(this._cookies);
    }

    public async getPersonalArtworksPage(page: number): Promise<PageResponse> {
        // pagination
        const limit = this._ARTWORK_PAGE_SIZE;
        const offset = limit * page;

        return (await this._privateApi.get(`${API_BASE_URL}/workshop/artworks/me?limit=${limit}&offset=${offset}`)) as PageResponse;
    }

    public async getArtworkImage(id: number): Promise<Blob> {
        const image = (await this._privateApi.getImage(`${API_BASE_URL}/workshop/artworks/${id}/image`));
        return image;
    }

    public async getArtwork(id: number): Promise<Artwork> {
        return (await this._privateApi.get(`${API_BASE_URL}/workshop/artworks/${id}`)) as Artwork;
    }
}