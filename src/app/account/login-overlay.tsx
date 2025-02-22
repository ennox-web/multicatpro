"use client";

import { useSession } from "next-auth/react";
import styles from './login-overlay.module.css';
import { authenticate } from "@/app/lib/actions";
import { ChangeEvent, useEffect, useState } from "react";

interface InputField {
    label: string;
    name: string;
    value: string;
    type: string;
    placeholder: string;
}

export default function LoginOverlay({ onClose }: { onClose: () => void }) {
    const [formValues, setFormValues] = useState({
        username: "",
        password: "",
    });
    const [formStyles, setFormStyles] = useState({
        username: styles.inputField,
        password: styles.inputField,
    })
    const { data: session } = useSession();
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    const inputFields: InputField[] = [
        {
            label: "Username",
            name: "username",
            type: "text",
            value: formValues.username,
            placeholder: "Username",
        },
        {
            label: "Password",
            name: "password",
            type: "password",
            value: formValues.password,
            placeholder: "Password",
        },
    ]

    function handleChange(event: ChangeEvent<HTMLInputElement>) {
        event.preventDefault();
        setFormValues({
            ...formValues,
            [event.target.name]: event.target.value,
        });
    }

    function setFormStyle(formType: string, isInvalid: boolean) {
        if (isInvalid) {
            setFormStyles((prevState) => {
                return {
                    ...prevState,
                    [formType]: styles.inputError,
                }
            });
            console.log(formStyles);
        }
        else {
            setFormStyles((prevState) => {
                return {
                    ...prevState,
                    [formType]: styles.inputField,
                }
            });
        }
    }

    async function formAction(formData: FormData) {
        const resp = await authenticate(formData);
        console.log(resp);
        if (resp === "Invalid credentials.") {
            console.log("Oh no!");
        }
        else {
            onClose();
        }
    }

    useEffect(() => {
        setFormStyle(
            "username",
            formValues.username.length < 4 || !isNaN(Number(formValues.username.charAt(0)))
        )

        setFormStyle(
            "password",
            formValues.password.length < 6 || formValues.password.length > 20
        )
    }, [formValues.username, formValues.password]);

    return (
        <form action={formAction} className={styles.loginForm}>
            <h1>Sign In</h1>
            {
                inputFields.map((field) => {
                    return (
                        <div className={styles.field} key={field.name}>
                            <label htmlFor={field.name}>{field.label}</label>
                            <input
                                id={field.name}
                                type={field.type}
                                name={field.name}
                                placeholder={field.placeholder}
                                required
                                className={formStyles[field.name]}
                                onChange={handleChange}
                            />
                        </div>
                    )
                })
            }
            <button className={`${styles.signInBtn} ${styles.userBtns}`}>Sign In</button>
        </form>
    );
}
