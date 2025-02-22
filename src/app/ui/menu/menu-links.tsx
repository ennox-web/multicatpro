import Link from "next/link";
import styles from "./menu-links.module.css";

interface MenuItemInterface {
    name: string;
    to: string;
    icon: string;
    dataCy: string;
}

const links: MenuItemInterface[] = [
    {
        name: "Overview",
        to: "/overview",
        icon: "home",
        dataCy: "menu-item-overview"
    },
    {
        name: "Projects",
        to: "/projects",
        icon: "space_dashboard",
        dataCy: "menu-item-projects"
    },
    {
        name: "Goals",
        to: "/goals",
        icon: "checklist",
        dataCy: "menu-item-goals"
    }
]


export default function MenuLinks() {
    return (
        <div className={styles.menuItems}>
            {
                links.map((link) => {
                    return (
                        <Link href={link.to} className={styles.menuItem} key={link.name}>
                            <span className={`material-symbols-outlined ${styles.icon}`}>{link.icon}</span>
                            <h4>{link.name}</h4>
                        </Link>
                    )
                })
            }
        </div>
    )
}
