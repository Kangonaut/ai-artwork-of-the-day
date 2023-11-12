import { CalDavSettingsApi } from '$lib/server/apis/caldav-settings-api';

export const load = async ({ cookies }) => {
    const settingsApi = new CalDavSettingsApi(cookies);

    try {

        const response = await settingsApi.get();
        return {
            settings: response,
        };
    } catch (error: any) {
        if (error?.status === 404)
            return { settings: null };
        else
            throw error;
    }
};

export const actions = {
    apply: async ({ request, cookies }) => {
        const settingsApi = new CalDavSettingsApi(cookies);

        // get form data
        const formData = await request.formData();
        const settings = {
            caldav_url: String(formData.get("caldav_url")),
            calendar_url: String(formData.get("calendar_url")),
            username: String(formData.get("username")),
            password: String(formData.get("password")),
        } as CalDavSettings;

        // check if settings already exist
        const isNew: boolean = JSON.parse(formData.get("isNew") as string);
        if (isNew)
            await settingsApi.create(settings);
        else
            await settingsApi.update(settings);
    },
    disable: async ({ cookies }) => {
        const settingsApi = new CalDavSettingsApi(cookies);
        await settingsApi.delete();
    }
}