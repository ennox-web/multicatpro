import TagChip from "./tag-chip";
import styles from "./tag-chip-list.module.css";

export default function TagChipList({ tags, rowIndex }: { tags: string[], rowIndex: number }) {
    return (
        <div className={styles.tagList}>
            {tags.map((tag) => {
                return (
                    <TagChip tagName={tag} styleType={rowIndex} />
                )
            })}
        </div>
    )
}