import { DaytimeSettingsApi } from '$lib/server/apis/daytime-settings-api';

export const load = async ({ cookies }) => {
    const settingsApi = new DaytimeSettingsApi(cookies);

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
        const settingsApi = new DaytimeSettingsApi(cookies);

        // get form data
        const formData = await request.formData();
        const settings = {
            timezone_hour_offset: Number(formData.get("timezoneHourOffset")),
        } as DaytimeSettings;

        // check if settings already exist
        const isNew: boolean = JSON.parse(formData.get("isNew") as string);
        if (isNew)
            await settingsApi.create(settings);
        else
            await settingsApi.update(settings);
    },
    disable: async ({ cookies }) => {
        const settingsApi = new DaytimeSettingsApi(cookies);
        await settingsApi.delete();
    }
}