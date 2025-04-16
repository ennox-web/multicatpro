import styles from "./page.module.css";

// Overall:
// TODO: Update "Add" buttons to be a plus icon in the top right corner of the widgets

// Project Block:
// TODO: Add functionality to "UpdateProjectButton"
// TODO: Add functionality to "Add Project" Buttons
// TODO: Make the Project Name in "project block" a button for users to click on to view details in a modal

// Project Table:
// TODO: Drag and Drop?
// TODO: Server-side sorting - https://tanstack.com/table/v8/docs/guide/sorting
// TODO: Pagination
// TODO: Number of projects to show

// Goals:
// TODO: Add functionality to "Add Goal" Buttons
// TODO: Add functionality to Goal button
// TODO: Add pin functionality to update goal pinned status and reorder goals as necessary
// (must add function to Goal Block List and pass down)


export default function Home() {
    return (
        <div className={styles.page}>
            <div>
                Home Page
            </div>
        </div>
    );
}
