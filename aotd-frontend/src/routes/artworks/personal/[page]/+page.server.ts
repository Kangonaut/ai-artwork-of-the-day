import { ArtworkApi } from "$lib/server/apis/artwork-api";
import type { Artwork } from "$lib/types/artwork";


export const load = async ({ cookies, params }) => {
    const page: number = parseInt(params.page);

    const artworkApi = new ArtworkApi(cookies);
    const pageResponse = await artworkApi.getPersonalArtworksPage(page);
    const artworks = pageResponse.results as Artwork[];

    return {
        page: {
            page: page,
            next: pageResponse.next !== null,
            previous: pageResponse.previous !== null,
        },
        artworks: artworks,
    };
};