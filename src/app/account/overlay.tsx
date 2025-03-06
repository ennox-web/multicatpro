import { createPortal } from 'react-dom';
import styles from './overlay.module.css';

export default function Overlay({children, onClose}: {children: React.ReactNode, onClose: () => void}) {
    const overlayContent = (
        <section className={styles.overlayContainer}>
            <button
                className={styles.overlayBackground}
                onClick={onClose}
                data-cy="overlay-bg"
                type="button"
                aria-label="close"
            />
            <div className={styles.overlayBody}>
                {children}
            </div>
        </section>
    );

    return createPortal(overlayContent, document.body);
}