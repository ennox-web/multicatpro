"use client";

import Link from 'next/link';
import styles from './user-menu.module.css';
import { useSession } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';

interface MenuLink {
    name: string;
    path: string;
    style: string;
}

interface UserMenuLinks {
    [key: string]: MenuLink[];
}

const userMenuLinks: UserMenuLinks = {
    "loggedOut": [
        {
            name: "Sign In",
            path: "/account/login",
            style: styles.signInBtn,
        },
        {
            name: "Create an Account",
            path: "/account/signup",
            style: styles.createAccount,
        },
    ],
    "loggedIn": [
        {
            name: "Settings",
            path: "/account/settings",
            style: styles.settings,
        },
    ],
}

function UserMenuDropdown({ loggedIn }: { loggedIn: boolean }) {
    const links = loggedIn ? userMenuLinks.loggedIn : userMenuLinks.loggedOut;

    return (
        <div className={styles.menuDropdown}>
            <div className={styles.dropDownContent}>
                {links.map((link) => <Link href={link.path} className={link.style} key={link.name}>{link.name}</Link>)}
            </div>
        </div>
    )
}


export default function UserMenu() {
    const { data: session } = useSession();
    const router = useRouter();
    const [showMenu, setShowMenu] = useState(false);
    const [loggedIn, setLoggedIn] = useState(false);

    function onClick() {
        if (!!session && !!session.user["username"]) {
            console.log("Here!");
        } else {
            router.push('/account/login')
        }
    }

    return (
        <div>
            <button
                className={styles.userButton}
                onClick={onClick}
                onMouseEnter={() => { setShowMenu(true) }}
                onMouseLeave={() => { setShowMenu(false) }}
            >
                <span className={`material-symbols-outlined ${styles.icon}`}>person</span>
            </button>
            {showMenu && (
                <div
                    onMouseEnter={() => { setShowMenu(true) }}
                    onMouseLeave={() => { setShowMenu(false) }}
                >
                    <UserMenuDropdown loggedIn={!!session ? !!session.user["username"] : false} />
                </div>
            )}
        </div>
    );
}
