import TagChip from "./tag-chip";
import styles from "./tag-chip-list.module.css";

export default function TagChipList({ tags, rowIndex, style = "" }: { tags: string[], rowIndex: number, style?: string }) {
    return (
        <div className={styles.tagList}>
            {tags.map((tag) => {
                const styleType = rowIndex % 2 ? 'tertiary' : 'primary';
                return (
                    <TagChip key={tag + rowIndex} tagName={tag} style={style ? style : styleType} />
                )
            })}
        </div>
    )
}