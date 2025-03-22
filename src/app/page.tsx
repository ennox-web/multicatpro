import styles from "./page.module.css";
import ProjectPriorities from "./ui/widget/project-priorities/project-priorities";

export default function Home() {
    return (
        <div className={styles.page}>
            <div>
                <ProjectPriorities />
            </div>
        </div>
    );
}
