export enum ActivityStatus {
    NotStarted = "not_started",
    InProgress = "in_progress",
    Completed = "completed",
}

export const ActivityStatusNames: Record<ActivityStatus, string> = {
    [ActivityStatus.NotStarted]: "",
    [ActivityStatus.InProgress]: "In Progress",
    [ActivityStatus.Completed]: "Completed",
};
export const ActivityStatusColors: Record<ActivityStatus, string> = {
    [ActivityStatus.NotStarted]: "bg-gray-500",
    [ActivityStatus.InProgress]: "bg-blue-500",
    [ActivityStatus.Completed]: "bg-green-500",
};
