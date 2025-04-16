import styles from './tag-chip.module.css';

export default function TagChip({ tagName, style = "primary" }: { tagName: string, style: string }) {
    var tagStyle = `${styles.tagBase}`;

    switch (style) {
        case "primary":
            tagStyle += ` ${styles.primary}`;
            break;
        case "tertiary":
            tagStyle += ` ${styles.tertiary}`;
            break;
        case "triadic":
            tagStyle += ` ${styles.triadic}`;
            break;
        case "secondary":
            tagStyle += ` ${styles.secondary}`;
            break;
    }
    return (
        <div className={tagStyle}>{tagName}</div>
    )
}