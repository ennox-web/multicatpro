import React from "react";
import styles from './component-wrapper.module.css'

export default function ComponentWrapper({children}: {children: React.ReactNode}) {
    return (
        <div className={styles.wrapper}>{children}</div>
    )
}