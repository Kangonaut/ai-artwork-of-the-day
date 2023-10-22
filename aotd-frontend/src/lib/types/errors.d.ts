export class AccessTokenExpiredError extends Error {
    constructor() {
        super("the access-token has expired");
        this.name = "AccessTokenExpiredError";
    }
}

export class UnauthorizedApiError extends Error {
    constructor(message: string) {
        super(message);
        this.name = "UnauthorizedApiError";
    }
}

export class UnexpectedApiError extends Error {
    constructor(message: string) {
        super(message);
        this.name = "UnexpectedApiError";
    }
}