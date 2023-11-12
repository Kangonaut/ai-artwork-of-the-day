import { PrivateArtworkApi } from "$lib/server/apis/private-artwork-api";
import type { PrivateArtwork } from "$lib/types/artwork";


export const load = async ({ cookies, params }) => {
    const page: number = parseInt(params.page);

    const artworkApi = new PrivateArtworkApi(cookies);
    const pageResponse = await artworkApi.getPersonalArtworksPage(page);
    const artworks = pageResponse.results as PrivateArtwork[];

    return {
        page: {
            page: page,
            next: pageResponse.next !== null,
            previous: pageResponse.previous !== null,
        },
        artworks: artworks,
    };
};