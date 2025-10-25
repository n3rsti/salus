export interface Program {
    id: number;
    name: string;
    duration_days: number;
    description: string;
    language: string;
    image: string;
    progress?: number;
    rating?: number;
}
