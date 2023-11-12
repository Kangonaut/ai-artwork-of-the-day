import type { Cookies } from "@sveltejs/kit";
import { PrivateApi } from "./private-api";
import { API_BASE_URL } from "$env/static/private";
import type { PrivateArtwork, PublicArtwork } from "$lib/types/artwork";

export class PublicArtworkApi {
    private readonly _ARTWORK_PAGE_SIZE: number = 9;

    private _privateApi: PrivateApi;

    constructor(private _cookies: Cookies) {
        this._privateApi = new PrivateApi(this._cookies);
    }

    public async getPublicArtworksPage(page: number): Promise<PageResponse> {
        // pagination
        const limit = this._ARTWORK_PAGE_SIZE;
        const offset = limit * page;

        return (await this._privateApi.get(`${API_BASE_URL}/workshop/public-artworks?limit=${limit}&offset=${offset}`)) as PageResponse;
    }

    public async getArtworkImage(id: number): Promise<Blob> {
        const image = (await this._privateApi.getImage(`${API_BASE_URL}/workshop/public-artworks/${id}/image`));
        return image;
    }

    public async getArtwork(id: number): Promise<PublicArtwork> {
        return (await this._privateApi.get(`${API_BASE_URL}/workshop/public-artworks/${id}`)) as PublicArtwork;
    }
}