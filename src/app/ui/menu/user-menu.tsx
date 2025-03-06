"use client";

import Link from 'next/link';
import styles from './user-menu.module.css';
import { useSession } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import { useState } from 'react';
import Overlay from '@/app/account/overlay';
import LoginOverlay from '@/app/account/login-overlay';
import { logout } from '@/app/lib/actions';
import SignupOverlay from '@/app/account/signup-overlay';

interface MenuLink {
    name: string;
    onClick: () => void;
    style: string;
}

interface UserMenuLinks {
    [key: string]: MenuLink[];
}

function UserMenuDropdown({ loggedIn, userMenuLinks }: { loggedIn: boolean, userMenuLinks: UserMenuLinks }) {
    const links = loggedIn ? userMenuLinks.loggedIn : userMenuLinks.loggedOut;

    return (
        <div className={styles.menuDropdown}>
            <div className={styles.dropDownContent}>
                {links.map((link) => <button className={link.style} key={link.name} onClick={link.onClick}>{link.name}</button>)}
            </div>
        </div>
    )
}

export default function UserMenu() {
    const { data: session } = useSession();
    const router = useRouter();
    const [showMenu, setShowMenu] = useState(true);
    const [showOverlayType, setShowOverlayType] = useState('');

    function onClick() {
        if (!!session && !!session.user["username"]) {
            console.log("Here!");
        } else {
            router.push('/account/login')
        }
    }

    const closeOverlay = () => {setShowOverlayType('')}

    const userMenuLinks: UserMenuLinks = {
        "loggedOut": [
            {
                name: "Sign In",
                onClick: () => { setShowOverlayType('login') },
                style: `${styles.signInBtn} ${styles.userBtns}`,
            },
            {
                name: "Create an Account",
                onClick: () => { setShowOverlayType('signup') },
                style: `${styles.createAccount} ${styles.userBtns}`,
            },
        ],
        "loggedIn": [
            {
                name: "Settings",
                onClick: () => { router.push("/account/settings") },
                style: `${styles.userBtns} ${styles.settingsBtn}`,
            },
            {
                name: "Logout",
                onClick: () => { logout() },
                style: `${styles.userBtns} ${styles.settingsBtn}`,
            },
        ],
    }

    return (
        <div>
            <button
                className={styles.userButton}
                onClick={onClick}
                onMouseEnter={() => { setShowMenu(true) }}
                onMouseLeave={() => { setShowMenu(true) }}
            >
                <span className={`material-symbols-outlined ${styles.icon}`}>person</span>
            </button>
            {showMenu && (
                <div
                    onMouseEnter={() => { setShowMenu(true) }}
                    onMouseLeave={() => { setShowMenu(true) }}
                >
                    <UserMenuDropdown loggedIn={!!session ? !!session.user["username"] : false} userMenuLinks={userMenuLinks} />
                </div>
            )}
            {showOverlayType === 'login' && (
                <Overlay onClose={closeOverlay}>
                    <LoginOverlay
                        onClose={closeOverlay}
                        createAccount={() => { setShowOverlayType('signup') }}
                    />
                </Overlay>
            )}
            {showOverlayType === 'signup' && (
                <Overlay onClose={closeOverlay}>
                    <SignupOverlay />
                </Overlay>
            )}
        </div>
    );
}
