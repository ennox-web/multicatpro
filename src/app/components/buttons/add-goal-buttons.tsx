import styles from './add-project-buttons.module.css';

export default function AddGoalButtons() {
    return (
        <div className={styles.projectButtons}>
            <button className={styles.button}>Add Goal</button>
            <button className={styles.button}>View more</button>
        </div>
    )
}