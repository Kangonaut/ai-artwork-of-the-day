import { ArtworkApi } from "$lib/server/apis/artwork-api";

export const load = async ({ cookies, params }) => {
    const id = Number(params.id);

    const artworkApi = new ArtworkApi(cookies);
    const artwork = await artworkApi.getArtwork(id);

    return {
        artwork: artwork,
    };
};