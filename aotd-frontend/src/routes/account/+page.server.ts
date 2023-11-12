import { CalDavSettingsApi } from '$lib/server/apis/caldav-settings-api';
import { DaytimeSettingsApi } from '$lib/server/apis/daytime-settings-api';
import { WeatherSettingsApi } from '$lib/server/apis/weather-settings-api';

export const load = async ({ cookies }) => {
    const daytimeSettingsApi = new DaytimeSettingsApi(cookies);
    const weatherSettingsApi = new WeatherSettingsApi(cookies);
    const calDavSettingsApi = new CalDavSettingsApi(cookies);

    return {
        isDaytimeEnabled: (await daytimeSettingsApi.head()).ok,
        isWeatherEnabled: (await weatherSettingsApi.head()).ok,
        isCalDavEnabled: (await calDavSettingsApi.head()).ok,
    };
};