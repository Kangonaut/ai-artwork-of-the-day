import { AuthApi } from "$lib/server/apis/auth-api";
import type { Actions } from "@sveltejs/kit";

export const actions: Actions = {
    default: async ({ cookies, request, fetch }) => {
        // retrieve form data
        const data = await request.formData();
        const username = data.get("username") as string;
        const password = data.get("password") as string;

        const authApi = new AuthApi(cookies);
        return await authApi.login(username, password);
    }
}