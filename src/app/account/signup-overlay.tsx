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

export default function SignupOverlay() {
    const [formValues, setFormValues] = useState({
        username: "",
        email: "",
        password: "",
        repassword: "",
    });
    const [formStyles, setFormStyles] = useState({
        username: styles.inputField,
        email: styles.inputField,
        password: styles.inputField,
        repassword: styles.inputField,
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
            label: "Email",
            name: "email",
            type: "email",
            value: formValues.email,
            placeholder: "Email",
        },
        {
            label: "Password",
            name: "password",
            type: "password",
            value: formValues.password,
            placeholder: "Password",
        },
        {
            label: "Verify Password",
            name: "repassword",
            type: "password",
            value: formValues.repassword,
            placeholder: "Verify password",
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

    useEffect(() => {
        setFormStyle(
            "username",
            formValues.username.length < 6 || !isNaN(Number(formValues.username.charAt(0)))
        )

        setFormStyle(
            "password",
            formValues.password.length < 6 || formValues.password.length > 20
        )

        setFormStyle(
            "repassword",
            formValues.repassword.length < 6 || formValues.repassword.length > 20 || formValues.repassword !== formValues.password
        )
        setFormStyle(
            "email",
            !formValues.email || !emailRegex.test(formValues.email)
        )
    }, [formValues.username, formValues.email, formValues.password, formValues.repassword]);

    return (
        <form action={(form) => { authenticate(form) }} className={styles.loginForm}>
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
            <button>Sign In</button>
        </form>
    );
}
