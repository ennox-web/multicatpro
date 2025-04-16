import ComponentWrapper from "@/app/components/wrappers/component-wrapper";

import styles from './goals.module.css';
import GoalsBlockList from "@/app/components/goals/goals-block-list";
import { goalTestData } from "@/app/api/data/goal-data";
import AddGoalButtons from "@/app/components/buttons/add-goal-buttons";

export default function Goals({ max = 3 }: { max?: number }) {
    var goalData = goalTestData;
    if (max > 0) {
        goalData.sort((a, b) => b.pinned ? 1 : -1);
        goalData = goalData.slice(0, max);
    }
    return (
        <div className={styles.wrapper}>
            <ComponentWrapper>
                <div className={styles.goals}>
                    <h3>Goals</h3>
                    <GoalsBlockList goalsList={goalData} />
                    <AddGoalButtons />
                </div>
            </ComponentWrapper>
        </div>
    )
}