export interface Program {
    id: number;
    name: string;
    duration: number;
    description: string;
    language: string;
    image: string;
    progress?: number;
    rating?: number;
}
