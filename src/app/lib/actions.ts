"use server";
import { AuthError } from "next-auth";

import { auth, signIn, signOut } from "@/auth";
import { graphqlRequest } from "../api/graphql_utils";

export async function authenticate(formData: FormData) {
    try {
        console.log(formData);
        const user = { username: formData.get("username"), password: formData.get("password"), redirectTo: "/" };
        await signIn('credentials', user);
    } catch (error) {
        if (error instanceof AuthError) {
            switch (error.type) {
                case 'CredentialsSignin':
                    console.log("Here?", error.type);

                    return 'Invalid credentials.';
                default:
                    return 'Something went wrong.';
            }
        }
    }
    return "Success";
}

export async function logout() {
    await signOut({ redirectTo: "/" });
}

export async function signUp(formData: FormData) {
    console.log(formData);
    const query = `
        mutation RegisterNewUser($userInput: UserInput!) {
            user {
                registerNewUser(userInput: $userInput) {
                    id
                    email
                    username
                }
            }
        }
    `;
    const variables = {
        userInput: {
            email: formData.get("email"),
            username: formData.get("username"),
            password: formData.get("password"),
        }
    }
    const response = await graphqlRequest({graphql_query: query, graphql_variables: variables});
}

export async function getUser() {
    const session = await auth();
    return session.user;
}
