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

interface PageResponse {
    count: number;
    next?: string;
    previous?: string;
    results: any[];
}