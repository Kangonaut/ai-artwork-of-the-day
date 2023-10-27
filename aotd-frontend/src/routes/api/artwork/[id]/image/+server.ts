import { PrivateArtworkApi } from "$lib/server/apis/personal-artwork-api";
import type { RequestHandler } from "@sveltejs/kit";

export const GET: RequestHandler = async ({ cookies, params }) => {
    const privateArtworkApi = new PrivateArtworkApi(cookies);
    const id = (params as any).id as number;
    const image = await privateArtworkApi.getArtworkImage(id);

    return new Response(image);
}