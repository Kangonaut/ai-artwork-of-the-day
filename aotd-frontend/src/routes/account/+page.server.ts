import { ArtstyleSettingsApi } from '$lib/server/apis/art-style-settings-api';
import { CalDavSettingsApi } from '$lib/server/apis/caldav-settings-api';
import { DaytimeSettingsApi } from '$lib/server/apis/daytime-settings-api';
import { PushoverSettingsApi } from '$lib/server/apis/pushover-settings-api.js';
import { WeatherSettingsApi } from '$lib/server/apis/weather-settings-api';

export const load = async ({ cookies }) => {
    const daytimeSettingsApi = new DaytimeSettingsApi(cookies);
    const weatherSettingsApi = new WeatherSettingsApi(cookies);
    const calDavSettingsApi = new CalDavSettingsApi(cookies);
    const artStylesSettingsApi = new ArtstyleSettingsApi(cookies);
    const pushoverSettingsApi = new PushoverSettingsApi(cookies);

    return {
        isDaytimeEnabled: (await daytimeSettingsApi.head()).ok,
        isWeatherEnabled: (await weatherSettingsApi.head()).ok,
        isCalDavEnabled: (await calDavSettingsApi.head()).ok,
        isArtStylesEnabled: (await artStylesSettingsApi.get()).art_styles.length !== 0,
        isPushoverEnabled: (await pushoverSettingsApi.head()).ok,
    };
};