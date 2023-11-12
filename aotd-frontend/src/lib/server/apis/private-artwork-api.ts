import type { Cookies } from "@sveltejs/kit";
import { PrivateApi } from "./private-api";
import { API_BASE_URL } from "$env/static/private";
import type { PrivateArtwork } from "$lib/types/artwork";

export class PrivateArtworkApi {
    private readonly _ARTWORK_PAGE_SIZE: number = 9;

    private _privateApi: PrivateApi;

    constructor(private _cookies: Cookies) {
        this._privateApi = new PrivateApi(this._cookies);
    }

    public async getPersonalArtworksPage(page: number): Promise<PageResponse> {
        // pagination
        const limit = this._ARTWORK_PAGE_SIZE;
        const offset = limit * page;

        return (await this._privateApi.get(`${API_BASE_URL}/workshop/private-artworks?limit=${limit}&offset=${offset}`)) as PageResponse;
    }

    public async getArtworkImage(id: number): Promise<Blob> {
        const image = (await this._privateApi.getImage(`${API_BASE_URL}/workshop/private-artworks/${id}/image`));
        return image;
    }

    public async getArtwork(id: number): Promise<PrivateArtwork> {
        return (await this._privateApi.get(`${API_BASE_URL}/workshop/private-artworks/${id}`)) as PrivateArtwork;
    }

    public async setArtworkVisibility(id: number, publish: boolean): Promise<PrivateArtwork> {
        return (await this._privateApi.put(`${API_BASE_URL}/workshop/private-artworks/${id}/publish/`, {
            publish: publish,
        })) as PrivateArtwork;
    }
}