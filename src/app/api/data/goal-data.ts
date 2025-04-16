import { ProjectInterface, projectTestData } from "./project-data";

export enum GoalType {
    COMPLETED = "COMPLETED",
    PROGRESS = "PROGRESS",
}

export enum Frequency {
    DAY = "DAY",
    WEEK = "WEEK",
    MONTH = "MONTH",
}

export enum Basis {
    DAILY = "DAILY",
    WEEKLY = "WEEKLY",
    MONTHLY = "MONTHLY",
    ANNUALLY = "ANNUALLY",
}

export interface GoalInterface {
    id: string;
    name: string;
    projects: ProjectInterface[];
    lastUpdate: Date;
    active: boolean;
    completed: boolean;
    progress: number;
    startDate: Date;

    basis: Basis;
    goalType: GoalType;
    target: number;
    projectType?: string;
    tags?: string[];
    frequency?: Frequency;
    targetFrequency?: number;
    targetDate: Date;
    pinned: boolean;
}

export const goalTestData: GoalInterface[] = [
    {
        id: "1",
        name: "Crochet Progress",
        projects: [projectTestData[0]],
        lastUpdate: new Date(2025, 3, 3, 15, 25, 0),
        active: true,
        completed: false,
        goalType: GoalType.PROGRESS,
        target: 1,
        progress: 0,
        startDate: new Date(2025, 2, 5, 12, 15, 0),

        basis: Basis.DAILY,
        projectType: "Crochet",
        tags: ["Wooble", "Gift"],
        targetFrequency: 3,
        targetDate: new Date(2025, 3, 30, 0, 0, 0),
        pinned: false,
    },
    {
        id: "2",
        name: "Writing Progress",
        projects: [projectTestData[2]],
        lastUpdate: new Date(2025, 3, 3, 15, 25, 0),
        active: true,
        completed: true,
        goalType: GoalType.PROGRESS,
        target: 1,
        progress: 1,
        startDate: new Date(2025, 2, 5, 12, 15, 0),

        frequency: Frequency.DAY,
        basis: Basis.WEEKLY,
        projectType: "Writing",
        tags: ["Chapter"],
        targetFrequency: 3,
        targetDate: new Date(2025, 4, 25, 0, 0, 0),
        pinned: false,
    },
    {
        id: "3",
        name: "Painting",
        projects: [projectTestData[1], projectTestData[4]],
        lastUpdate: new Date(2025, 3, 2, 18, 25, 0),
        active: true,
        completed: true,
        goalType: GoalType.COMPLETED,
        target: 2,
        progress: 2,
        startDate: new Date(2025, 2, 5, 12, 15, 0),

        frequency: Frequency.WEEK,
        basis: Basis.MONTHLY,
        projectType: "Painting",
        tags: ["D&D"],
        targetFrequency: 3,
        targetDate: new Date(2025, 12, 25, 0, 0, 0),
        pinned: true,
    },
    {
        id: "4",
        name: "Overall Projects",
        projects: [projectTestData[1], projectTestData[4]],
        lastUpdate: new Date(2025, 3, 2, 18, 25, 0),
        active: true,
        completed: false,
        goalType: GoalType.COMPLETED,
        target: 12,
        progress: 2,
        startDate: new Date(2025, 2, 5, 12, 15, 0),
        tags: ["Fantasy"],
        basis: Basis.ANNUALLY,
        targetDate: new Date(2025, 12, 25, 0, 0, 0),
        pinned: true,
    },
]