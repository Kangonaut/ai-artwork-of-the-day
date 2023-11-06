import { ArtworkApi } from "$lib/server/apis/artwork-api";
import type { RequestHandler } from "@sveltejs/kit";

export const GET: RequestHandler = async ({ cookies, params }) => {
    const artworkApi = new ArtworkApi(cookies);
    const id = (params as any).id as number;
    const image = await artworkApi.getArtworkImage(id);

    return new Response(image);
}