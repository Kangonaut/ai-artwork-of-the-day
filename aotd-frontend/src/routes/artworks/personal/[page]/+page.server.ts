import { PrivateArtworkApi } from "$lib/server/apis/personal-artwork-api";
import type { Actions } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";
import type { Artwork } from "$lib/types/artwork";


export const load = async ({ cookies, params }) => {
    const page: number = parseInt(params.page);

    const privateArtworkApi = new PrivateArtworkApi(cookies);
    const pageResponse = await privateArtworkApi.getArtworksPage(page);
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