import type { User } from "./user.model";

export interface Review {
    id: number;
    content_id: number;
    content_type: "program" | "activity";
    rating: number;
    comment: string;
    user: User;
    created_at: Date;
}
