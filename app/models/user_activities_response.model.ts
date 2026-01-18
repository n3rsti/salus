import type { Activity } from "./activity.model";
import type { Program } from "./program.model";

export interface UserActivitiesResponse {
    activities: UserActivity[];
    programs: ProgramWithActivities[];
    limit: number;
    offset: number;
    has_more: boolean;
}

export interface ProgramWithActivities extends Program {
    user_activities: Record<string, number>;
    owner_username: string;
}

export interface UserActivity {
    id: number;
    owner_id: number;
    owner_username: string;
    activity_id: number | null;
    program_id: number | null;
    program_day_id: number | null;
    start_date: Date;
    end_date: Date;
    activity: Activity | null;
}
