import { PublicArtworkApi } from "$lib/server/apis/public-artwork-api";

export const load = async ({ cookies, params }) => {
    const id = Number(params.id);

    const artworkApi = new PublicArtworkApi(cookies);
    const artwork = await artworkApi.getArtwork(id);

    return {
        artwork: artwork,
    };
};