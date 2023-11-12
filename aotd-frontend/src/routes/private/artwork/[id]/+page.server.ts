import { PrivateArtworkApi } from "$lib/server/apis/private-artwork-api";

export const load = async ({ cookies, params }) => {
    const id = Number(params.id);

    const artworkApi = new PrivateArtworkApi(cookies);
    const artwork = await artworkApi.getArtwork(id);

    return {
        artwork: artwork,
    };
};

export const actions = {
    publish: async ({ cookies, params }) => {
        const artworkApi = new PrivateArtworkApi(cookies);

        const id = Number(params.id);
        await artworkApi.setArtworkVisibility(id, true);
    },
    hide: async ({ cookies, params }) => {
        const artworkApi = new PrivateArtworkApi(cookies);

        const id = Number(params.id);
        await artworkApi.setArtworkVisibility(id, false);
    },
};