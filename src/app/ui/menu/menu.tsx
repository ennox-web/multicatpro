import MenuLinks from "./menu-links";
import styles from "./menu.module.css";
import UserMenu from "./user-menu";
import Link from "next/link";

export default function Menu() {
    return (
        <div className={styles.menuContainer}>
            <Link href="/"><h3 className={styles.title}>MultiCatPro</h3></Link>
            <MenuLinks />
            <UserMenu />
        </div>
    )
}
