import { ArtstyleSettingsApi as ArtStyleSettingsApi } from '$lib/server/apis/art-style-settings-api';
import { redirect } from '@sveltejs/kit';

export const load = async ({ cookies }) => {
    const settingsApi = new ArtStyleSettingsApi(cookies);

    return {
        availableArtStyles: await settingsApi.getAvailableArtstyles(),
        settings: await settingsApi.get(),
    };
};

export const actions = {
    apply: async ({ request, cookies }) => {
        const settingsApi = new ArtStyleSettingsApi(cookies);

        
        // get form data
        const formData = await request.formData();
        const settings = {
            art_styles: formData.getAll("artStyles").map(str => Number(str))
        } as ArtStyleSettings;

        await settingsApi.update(settings);

        throw redirect(302, "/account");
    },
    disable: async ({ cookies }) => {
        const settingsApi = new ArtStyleSettingsApi(cookies);

        const settings: ArtStyleSettings = {
            art_styles: []
        }

        await settingsApi.update(settings);

        throw redirect(302, "/account");
    }
}