import { redirect, type Handle } from "@sveltejs/kit";

export const handle: Handle = async ({ event, resolve }) => {
    // // make user data available to all pages
    // (event.locals as any).user = userData;    

    if (event.url.pathname === "/login")
        throw redirect(302, "/auth/login");

    return resolve(event);
}