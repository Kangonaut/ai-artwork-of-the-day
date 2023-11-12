interface DaytimeSettings {
    timezone_hour_offset: number;
}

interface WeatherSettings {
    longitude: number;
    latitude: number;
}

interface CalDavSettings {
    caldav_url: string,
    calendar_url: string,
    username: string,
    password: string,
}