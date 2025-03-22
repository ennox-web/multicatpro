import ProjectTable from "@/app/components/project-table";

import styles from './project-priorities.module.css'
import ComponentWrapper from "@/app/components/component-wrapper";
import AddProjectButtons from "@/app/components/add-project-buttons";

export default function ProjectPriorities() {
    return (
        <ComponentWrapper>
            <div className={styles.priorities}>
                <h2>Project Priorities</h2>
                <ProjectTable />
                <AddProjectButtons />
            </div>
        </ComponentWrapper>
    )
}