import type { Handle } from "@sveltejs/kit";

export const handle: Handle = async ({ event, resolve }) => {
    const access = await event.cookies.get("access");

    const response = await fetch("http://localhost:8000/auth/users/me", {
        headers: {
            "Authorization": `JWT ${access}`,
        }
    });

    if (response.ok) {
        const user = await response.json();
        console.log(`loaded user: ${JSON.stringify(user)}`);
        (event.locals as any).user = user;
    }

    return resolve(event);
}