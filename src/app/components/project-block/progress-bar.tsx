import styles from './progress-bar.module.css';

export default function ProgressBar({ value }: { value: number }) {
    const percentage = value * 100;
    return (
        <div className={styles.barContainer}>
            <div className={styles.progressContainer}>
                <div className={styles.progressFill} style={{ width: `${percentage}%` }} />
            </div>
            <span className={styles.percentage}>{`${percentage.toFixed(0)}%`}</span>
        </div>
    )

}