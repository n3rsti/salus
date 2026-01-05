import type { ProgramDay } from "./program_day.model";
import type { User } from "./user.model";

export interface Program {
    id?: number;
    name: string;
    duration_days: number;
    description: string;
    language: string;
    image_url: string;
    progress?: number;
    rating?: number;
    days?: ProgramDay[];
    owner?: User;
}
