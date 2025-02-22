"use server";
import { AuthError } from "next-auth";

import {auth, signIn} from "@/auth";

export async function authenticate(formData: FormData) {
    try {
        console.log(formData);
        const user = {email: formData.get("email"), password: formData.get("password"), redirect: false};
        await signIn('credentials', user);
    } catch(error) {
        if(error instanceof AuthError) {
            switch (error.type) {
                case 'CredentialsSignin':
                  return 'Invalid credentials.';
                default:
                  return 'Something went wrong.';
              }
            }
        throw error;
    }
}

export async function getUser() {
    const session = await auth();
    return session.user;
}
