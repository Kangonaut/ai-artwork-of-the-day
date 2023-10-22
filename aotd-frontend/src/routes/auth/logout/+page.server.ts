import { AuthApi } from "$lib/apis/auth-api";
import { redirect, type Actions } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async () => {
    // only used as an API endpoint
    throw redirect(302, '/')
  }

export const actions: Actions = {
    default: async ({ cookies }) => {
        const authApi = new AuthApi(cookies);
        await authApi.logout();
    },
};