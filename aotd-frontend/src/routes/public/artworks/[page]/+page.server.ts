import { PublicArtworkApi } from "$lib/server/apis/public-artwork-api.js";
import type { PublicArtwork } from "$lib/types/artwork";


export const load = async ({ cookies, params }) => {
    const page: number = parseInt(params.page);

    const artworkApi = new PublicArtworkApi(cookies);
    const pageResponse = await artworkApi.getPublicArtworksPage(page);
    const artworks = pageResponse.results as PublicArtwork[];

    return {
        page: {
            page: page,
            next: pageResponse.next !== null,
            previous: pageResponse.previous !== null,
        },
        artworks: artworks,
    };
};