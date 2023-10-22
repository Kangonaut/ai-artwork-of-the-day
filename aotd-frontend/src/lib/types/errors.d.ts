class UnauthorizedApiError extends ApiError {
    async constructor(response: Response) {
        await super(response);
        this.name = "UnauthorizedApiError";
    }
}

class AccessTokenExpiredApiError extends Error {
    constructor() {
        super("the access-token has expired");
        this.name = "AccessTokenExpiredError";
    }
}



class ApiError extends Error {
    async constructor(response: Response) {unexpected 
        const detail = await response.json();
        super(`API error: ${response.status} - ${response.statusText} - ${detail}`);
        this.name = "ApiError";
    }
}