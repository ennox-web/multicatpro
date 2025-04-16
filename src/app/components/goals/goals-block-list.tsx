import { GoalInterface, goalTestData } from "@/app/api/data/goal-data";
import GoalsBlock from "./goals-block";
import styles from './goals-block-list.module.css';

export default function GoalsBlockList({ goalsList }: { goalsList: GoalInterface[] }) {
    return (
        <div className={styles.goalsList}>
            {
                goalsList.map((goal, index) => <GoalsBlock key={goal.name + index} goal={goal} />)
            }
        </div>
    )
}