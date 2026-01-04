type DifficultyName = "Easy" | "Moderate" | "Hard";
export interface Difficulty {
    name: DifficultyName;
    value: number;
}

export const Difficulties: Record<number, DifficultyName> = {
    1: "Easy",
    2: "Moderate",
    3: "Hard",
};

export const DifficultiesColors: Record<number, string> = {
    1: "bg-green-500",
    2: "bg-yellow-500",
    3: "bg-red-500",
};
