import { BASE_API_URL } from "$env/static/private";
import { error } from "console";

const API_URL: string = `${BASE_API_URL}/auth`;

interface LoginResponse {
    refresh: string;
    access: string;
}

interface ErrorResponse {
    detail: string;
}

export class AuthApi {
    constructor() { }

    public static async login(username: string, password: string): Promise<LoginResponse> {
        const requestBody = {
            username,
            password
        };

        const response = await fetch(`${API_URL}/jwt/create/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(requestBody),
        });

        const responseData: object = await response.json();

        if (response.ok)
            return responseData as LoginResponse;
        else
            throw new Error((responseData as ErrorResponse).detail);
    }
}