import styles from "./priority-icon.module.css"

enum Priority {
    Default = 0,
    Lower,
    Low,
    High,
    Higher,
}

interface PriorityIconType {
    icon: string;
    className: string;
}

const priorityIcons: { [id: number]: PriorityIconType } = {
    0: {
        icon: "horizontal_rule",
        className: `${styles.mediumPriority} ${styles.icon}`
    },
    1: {
        icon: "keyboard_double_arrow_down",
        className: `${styles.lowerPriority} ${styles.icon}`
    },
    2: {
        icon: "keyboard_arrow_down",
        className: `${styles.lowPriority} ${styles.icon}`
    },
    3: {
        icon: "keyboard_arrow_up",
        className: `${styles.highPriority} ${styles.icon}`
    },
    4: {
        icon: "keyboard_double_arrow_up",
        className: `${styles.higherPriority} ${styles.icon}`
    }
}

export default function PriorityIcon({ priority }: { priority: number }) {
    var index = priority;
    if (priority > 5 || priority < 0) {
        index = 0;
    }
    return (
        <span className={`material-symbols-outlined ${priorityIcons[index].className}`}>{priorityIcons[index].icon}</span>
    )
}