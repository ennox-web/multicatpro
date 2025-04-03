import { ProjectInterface } from "@/app/api/data/project-data";
import styles from './project-block.module.css';
import ProgressBar from "./progress-bar";
import UpdateProjectButton from "../buttons/update-project-button";

export default function ProjectBlock({ project }: { project: ProjectInterface }) {
    return (
        <div className={styles.projectBlock}>
            <div className={styles.projectBlockHeader}>
                <div className={styles.nameHeader}>
                    <h5 className={styles.projectName}>{project.name}</h5>
                    <h6 className={styles.projectType}>{project.projectType}</h6>
                </div>
                <UpdateProjectButton />
            </div>
            <ProgressBar value={project.progress} />
        </div>
    )
}