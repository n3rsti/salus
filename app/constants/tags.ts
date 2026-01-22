export enum Tag {
    Stress = 1,
    Workout = 2,
    Sleep = 3,
    Focus = 4,
    Mental_Health = 5,
}

export const TagNames: Record<Tag, string> = {
    [Tag.Stress]: "Stress",
    [Tag.Workout]: "Workout",
    [Tag.Sleep]: "Sleep",
    [Tag.Focus]: "Focus",
    [Tag.Mental_Health]: "Mental Health",
};

export const TagColors: Record<Tag, string> = {
    [Tag.Stress]: "bg-blue-500 shadow-blue-500/50",
    [Tag.Workout]: "bg-red-500 shadow-red-500/50",
    [Tag.Sleep]: "bg-purple-500 shadow-purple-500/50",
    [Tag.Focus]: "bg-yellow-500 shadow-yellow-500/50",
    [Tag.Mental_Health]: "bg-green-500 shadow-green-500/50",
};

export const TagIcons: Record<Tag, string> = {
    [Tag.Stress]: "streamline:brain-cognitive-solid",
    [Tag.Workout]: "solar:dumbbell-bold",
    [Tag.Sleep]: "ri:moon-fill",
    [Tag.Focus]: "material-symbols:target",
    [Tag.Mental_Health]: "material-symbols:digital-wellbeing-rounded",
};
