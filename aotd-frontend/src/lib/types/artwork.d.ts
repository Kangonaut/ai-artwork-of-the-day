import type { UserData } from "./user";

export interface PrivateArtwork {
    id: number;
    title: string;
    created_at: string;
    data: object;
    image_prompt: string;
    is_public: boolean;
}

export interface PublicArtwork {
    id: number;
    title: string;
    created_at: string;
    user: UserData;
}