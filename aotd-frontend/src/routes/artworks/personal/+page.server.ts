import { PrivateArtworkApi } from "$lib/server/apis/personal-artwork-api";
import type { Actions } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";


export const load = async ({ cookies }) => {

    const privateArtworkApi = new PrivateArtworkApi(cookies);
    const artworks = await privateArtworkApi.getArtworks();

    return {
        artworks: artworks,
    };
};