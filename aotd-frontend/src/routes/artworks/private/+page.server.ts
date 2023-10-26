import { PrivateArtworkApi } from "$lib/server/apis/private-artwork-api";
import type { PageServerLoad } from "./$types";


export const load = async ({ cookies }) => {
    const privateArtworkApi = new PrivateArtworkApi(cookies);
    const artworks = await privateArtworkApi.getArtworks();

    return {
        artworks: artworks
    };
};