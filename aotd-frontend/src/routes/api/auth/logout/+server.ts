import { AuthApi } from "$lib/server/apis/auth-api";
import type { RequestHandler } from "@sveltejs/kit";

export const POST: RequestHandler = async ({ cookies }) => {
    const authApi = new AuthApi(cookies);
    await authApi.logout();

    return new Response("successfully logged out!");
};