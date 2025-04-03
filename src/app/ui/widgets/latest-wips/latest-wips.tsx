import ComponentWrapper from "@/app/components/wrappers/component-wrapper";
import styles from './latest-wips.module.css';
import ProjectBlockList from "@/app/components/project-block/project-block-list";
import AddProjectButtons from "@/app/components/buttons/add-project-buttons";
import { projectTestData } from "@/app/api/data/project-data";

export default function LatestWIPs({ max = 3 }: { max?: number }) {
    var projectData = projectTestData;
    if (max > 0) {
        projectData.sort((a, b) => a.updatedOn.getTime() - b.updatedOn.getTime());
        projectData = projectData.slice(0, max);
    }

    return (
        <div className={styles.wrapper}>
            <ComponentWrapper>
                <div className={styles.latestWIPS}>
                    <h3>Latest WIPs</h3>
                    <ProjectBlockList projectList={projectData} />
                    <AddProjectButtons />
                </div>
            </ComponentWrapper>
        </div>
    )
}