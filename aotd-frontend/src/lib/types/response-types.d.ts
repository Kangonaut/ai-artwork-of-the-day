interface LoginResponse {
    refresh: string;
    access: string;
}

interface RefreshResponse {
    access: string;
}

interface ErrorResponse {
    detail: string;
}