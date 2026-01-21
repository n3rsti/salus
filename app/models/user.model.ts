import type { Role } from "~/constants/roles";

export interface User {
    username: string;
    role_id: Role;
    id: number;
}
