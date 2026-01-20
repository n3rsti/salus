import type { Tag } from "~/constants/tags";
import type { User } from "./user.model";

export interface Activity {
    id?: number;
    name: string;
    duration_minutes: number;
    description: string;
    difficulty: number;
    content?: string;
    average_rating?: number;
    image_url: string;
    owner?: User;
    tags?: Tag[];
    owner_id?: number;
    owner_username?: string;
}
