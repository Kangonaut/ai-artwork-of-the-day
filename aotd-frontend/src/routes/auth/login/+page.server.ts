import { redirect, type Actions, fail } from "@sveltejs/kit";
import { AuthApi } from "$lib/apis/auth-api";
import { AuthCookies } from "$lib/cookies/auth-cookies";

const AUTH_COOKIE_MAX_AGE = 60 * 60 * 24 * 7; // 7 days

interface LoginResponse {
    refresh: string;
    access: string;
}

interface ErrorResponse {
    details: string;
}

export const actions: Actions = {
    default: async ({ cookies, request, fetch }) => {
        // retrieve form data
        const data = await request.formData();
        const username = data.get("username") as string;
        const password = data.get("password") as string;

        // send login request
        try {

            const response: LoginResponse = await AuthApi.login(username, password);

            // set cookies
            const authCookies = new AuthCookies(cookies);
            authCookies.refreshToken = response.refresh;
            authCookies.accessToken = response.access;
        } catch (error) {
            if (error instanceof Error)
                return fail(400, { error: error.message });
            else
                throw error;
        }

        console.log("redirect");

        // redirect to user screen
        throw redirect(302, "/user/me");
    }
}