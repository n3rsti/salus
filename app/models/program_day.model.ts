import type { Activity } from "./activity.model";

export interface ProgramDay {
    id?: number;
    description: string;
    day_number: number;
    program_id: number;
    activities?: Activity[];
    activities_ids?: number[];
}
