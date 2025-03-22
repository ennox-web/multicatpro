import styles from './tag-chip.module.css';

export default function TagChip({ tagName, styleType }: { tagName: string, styleType: number }) {
    var tagStyle = '';
    if (styleType % 2) {
        tagStyle = `${styles.tagBase} ${styles.tag1}`;
    }
    else {
        tagStyle = `${styles.tagBase} ${styles.tag2}`;
    }
    return (
        <div className={tagStyle}>{tagName}</div>
    )
}