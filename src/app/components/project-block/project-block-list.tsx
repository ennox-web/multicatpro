import { ProjectInterface } from "@/app/api/data/project-data";
import ProjectBlock from "./project-block";
import styles from './project-block-list.module.css';

export default function ProjectBlockList({ projectList }: { projectList: ProjectInterface[] }) {
    return (
        <div className={styles.projectList}>
            {
                projectList.map((project) => {
                    return (
                        <ProjectBlock key={project.id} project={project} />
                    )
                })
            }
        </div>
    )
}