export interface TestInterface {
    id: number;
    name: string;
    category: string;
    price: number;
    inStock: boolean;
    rating: number;
}

export interface ProjectInterface {
    id: string;
    name: string;
    projectType: string;
    projectTemplateID: string;
    startedOn?: Date;
    completedOn?: Date;
    updatedOn: Date;
    tags: string[];
    priority: number;
    progress: number;
    steps: string[];
    activeStep: number;
}

export const projectTestData: ProjectInterface[] = [
    {
        id: "1",
        name: "Dino2",
        projectType: "Crochet",
        projectTemplateID: "1",
        updatedOn: new Date(2025, 3, 1, 10, 30, 0),
        tags: ["Wooble", "Crochet", "Gift"],
        priority: 1,
        progress: 1/3,
        steps: ["magic ring", "6 sc", "6 dc"],
        activeStep: 1,
    },
    {
        id: "2",
        name: "Zephyr",
        projectType: "Painting",
        projectTemplateID: "2",
        updatedOn: new Date(2025, 2, 25, 12, 12, 0),
        tags: ["D&D", "Vampire", "Current Campaign"],
        priority: 2,
        progress: 2/4,
        steps: ["prime", "Base coat", "Details", "Highlights"],
        activeStep: 2,
    },
    {
        id: "3",
        name: "First Light",
        projectType: "Writing",
        projectTemplateID: "3",
        updatedOn: new Date(2025, 3, 2, 21, 36, 0),
        tags: ["Chapter", "Fantasy", "Novel"],
        priority: 0,
        progress: 1/4,
        steps: ["Outline", "First Draft", "Second Draft", "Recording"],
        activeStep: 1,
    },
    {
        id: "4",
        name: "Dino",
        projectType: "Crochet",
        projectTemplateID: "1",
        updatedOn: new Date(2025, 2, 15, 18, 36, 0),
        tags: ["Wooble", "Crochet", "Gift"],
        priority: 3,
        progress: 1/3,
        steps: ["magic ring", "6 sc", "6 dc"],
        activeStep: 1,
    },
    {
        id: "5",
        name: "Giant Bat",
        projectType: "Painting",
        projectTemplateID: "2",
        updatedOn: new Date(2025, 2, 30, 13, 45, 0),
        tags: ["D&D", "Medium", "Monster", "Current Campaign"],
        priority: 4,
        progress: 2/4,
        steps: ["prime", "Base coat", "Details", "Highlights"],
        activeStep: 2,
    },
]

export const defaultData: TestInterface[] = [
    {
        "id": 1,
        "name": "Wireless Mouse",
        "category": "Electronics",
        "price": 29.99,
        "inStock": true,
        "rating": 4.5
    },
    {
        "id": 2,
        "name": "Bluetooth Keyboard",
        "category": "Electronics",
        "price": 49.99,
        "inStock": true,
        "rating": 4.0
    },
    {
        "id": 3,
        "name": "HD Monitor",
        "category": "Electronics",
        "price": 199.99,
        "inStock": false,
        "rating": 4.8
    },
    {
        "id": 4,
        "name": "Office Chair",
        "category": "Furniture",
        "price": 150.0,
        "inStock": true,
        "rating": 4.3
    },
    {
        "id": 5,
        "name": "Desk Lamp",
        "category": "Furniture",
        "price": 25.99,
        "inStock": false,
        "rating": 4.7
    }
];