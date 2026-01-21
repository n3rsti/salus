import type { User } from "./user.model";

export interface Request {
    id: number;
    description: string;
    user: User;
    admin?: User;
    resolved: boolean;
    created_at: Date;
    resolved_at: Date | null;
    response: string | null;
}
