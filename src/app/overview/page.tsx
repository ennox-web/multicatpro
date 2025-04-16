import Goals from '../ui/widgets/goals/goals';
import LatestWIPs from '../ui/widgets/latest-wips/latest-wips';
import ProjectPriorities from '../ui/widgets/project-priorities/project-priorities';

import styles from './page.module.css';

export default function Overview() {
    return (
        <div className={styles.page}>
            <div className={styles.widgetsWrapper}>
                <div className={styles.latestWips}>
                    <LatestWIPs max={4} />
                </div>
                <div className={styles.goals}>
                    <Goals max={3} />
                </div>

                <div className={styles.projectPriorities}>
                    <ProjectPriorities />
                </div>
            </div>
        </div>
    )
}