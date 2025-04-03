import styles from "./page.module.css";
import LatestWIPs from "./ui/widgets/latest-wips/latest-wips";
import ProjectPriorities from "./ui/widgets/project-priorities/project-priorities";

// TODO: Add functionality to "UpdateProjectButton"
// TODO: Add functionality to "Add Project" Buttons

// Project Table:
// TODO: Drag and Drop?
// TODO: Server-side sorting - https://tanstack.com/table/v8/docs/guide/sorting
// TODO: Pagination
// TODO: Number of projects to show

export default function Home() {
    return (
        <div className={styles.page}>
            <div>
                <LatestWIPs />
                <ProjectPriorities />
            </div>
        </div>
    );
}
