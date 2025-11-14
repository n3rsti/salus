export interface Activity {
    id?: number;
    name: string;
    duration_minutes: number;
    description: string;
    difficulty: number;
    rating?: number;
    image_url: string;
}
