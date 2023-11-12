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

interface ArtStyleSettings {
    art_styles: number[];
}

interface ArtStyle {
    id: number;
    name: string;
}

interface PushoverSettings {
    user_key: string;
}