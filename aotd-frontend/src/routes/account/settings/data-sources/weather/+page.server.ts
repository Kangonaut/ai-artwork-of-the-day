import { WeatherSettingsApi } from '$lib/server/apis/weather-settings-api';
import { redirect } from '@sveltejs/kit';

export const load = async ({ cookies }) => {
    const settingsApi = new WeatherSettingsApi(cookies);

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
        const settingsApi = new WeatherSettingsApi(cookies);

        // get form data
        const formData = await request.formData();
        const settings = {
            longitude: Number(formData.get("longitude")),
            latitude: Number(formData.get("latitude")),
        } as WeatherSettings;

        // check if settings already exist
        const isNew: boolean = JSON.parse(formData.get("isNew") as string);
        if (isNew)
            await settingsApi.create(settings);
        else
            await settingsApi.update(settings);

        throw redirect(302, "/account");
    },
    disable: async ({ cookies }) => {
        const settingsApi = new WeatherSettingsApi(cookies);
        await settingsApi.delete();

        throw redirect(302, "/account");
    }
}