import { redirect } from '@sveltejs/kit';
import { UserSettingsApi } from '$lib/server/apis/user-settings';

export const load = async ({ cookies }) => {
    const settingsApi = new UserSettingsApi(cookies);

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
        const settingsApi = new UserSettingsApi(cookies);

        // get form data
        const formData = await request.formData();
        const settings = {
            issue_time: formData.get("issueTime"),
        } as UserSettings;

        // check if settings already exist
        const isNew: boolean = JSON.parse(formData.get("isNew") as string);
        if (isNew)
            await settingsApi.create(settings);
        else
            await settingsApi.update(settings);

        throw redirect(302, "/account");
    },
    disable: async ({ cookies }) => {
        const settingsApi = new UserSettingsApi(cookies);
        await settingsApi.delete();

        throw redirect(302, "/account");
    }
}