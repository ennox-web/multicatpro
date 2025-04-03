import styles from './add-project-buttons.module.css'

export default function AddProjectButtons() {
    return (
        <div className={styles.projectButtons}>
            <button className={styles.button}>Add Project</button>
            <button className={styles.button}>View more</button>
        </div>
    )
}