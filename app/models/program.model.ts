import type { Tag } from "~/constants/tags";
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
    average_rating?: number;
    days?: ProgramDay[];
    owner?: User;
    tags?: Tag[];
}
