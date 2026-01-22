export interface UserActivity {
    id?: number;
    user_id: number;
    program_id?: number;
    program_day_id?: number;
    activity_id?: number;
    start_date: Date;
    end_date: Date;
}
