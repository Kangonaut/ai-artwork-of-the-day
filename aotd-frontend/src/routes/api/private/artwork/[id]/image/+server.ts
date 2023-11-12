import { PrivateArtworkApi } from "$lib/server/apis/private-artwork-api";
import type { RequestHandler } from "@sveltejs/kit";

export const GET: RequestHandler = async ({ cookies, params }) => {
    const artworkApi = new PrivateArtworkApi(cookies);
    const id = (params as any).id as number;
    const image = await artworkApi.getArtworkImage(id);

    return new Response(image);
}