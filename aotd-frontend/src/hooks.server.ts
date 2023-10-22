import { UserApi } from "$lib/apis/user-api";
import { AuthCookies } from "$lib/cookies/auth-cookies";
import { redirect, type Handle } from "@sveltejs/kit";

export const handle: Handle = async ({ event, resolve }) => {
    // check if logged in
    const _authCookies = new AuthCookies(event.cookies);
    if (_authCookies.isLoggedIn()) {
        // get user data
        const userApi = new UserApi(event.cookies);
        const userData = await userApi.getUserData();

        // make user data available to all pages
        (event.locals as any).user = userData;
    }

    // redirect legacy login route 
    if (event.url.pathname === "/login")
        throw redirect(302, "/auth/login");

    return resolve(event);
}