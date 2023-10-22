import { AuthApi } from "$lib/apis/auth-api";
import { AuthManager } from "$lib/managers/auth-manager";
import type { UserData } from "$lib/types/user";
import type { Handle } from "@sveltejs/kit";

export const handle: Handle = async ({ event, resolve }) => {
    const authManager: AuthManager = new AuthManager(event.cookies);
    const userData: UserData = await authManager.getUserData();

    // make user data available to all pages
    (event.locals as any).user = userData;    

    return resolve(event);
}