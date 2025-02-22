import NextAuth, { DefaultSession } from "next-auth";
import Credentials from "next-auth/providers/credentials";
// import Google from "next-auth/providers/google";
import { cookies } from "next/headers";

declare module "next-auth" {
    interface Session {
        user: {
            id: string;
            email: string;
            username: string;
            cognitoGroups: string[];
            accessToken: string;
            accessTokenExpires: number;
            role: string;
        } & DefaultSession["user"]
    }
}

async function refreshAccessToken(token: any) {
    // TODO: Update this to swap refresh.ts and implement refresh API route
    if (!token.refreshToken) {
        console.log("NO REFRESH TOKEN!")
        return {
            ...token,
            error: "NoRefreshToken",
        };
    }
    console.log("REFRESH TOKEN??: ", token.refreshToken);

    const response = await fetch(`${process.env.API_BASE_URL}/api/refresh`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token.refreshToken}`
        }
    })
        .then((response) => response)
        .catch((error) => console.error(error));

    if (response) {
        console.log("The token has been refreshed successfully.")

        const data = await response.json()
        console.log("Data?:", data);

        const decodedAccessToken = JSON.parse(Buffer.from(data["access_token"].split(".")[1], "base64").toString())

        return {
            ...token,
            accessToken: data["access_token"],
            refreshToken: data["refresh_token"] ?? token.refreshToken,
            idToken: "",
            accessTokenExpires: new Date(decodedAccessToken["exp"] * 1000),
            error: "",
        }
    }
    else {
        console.log("The token could not be refreshed!")
        return {
            ...token,
            error: "RefreshAccessTokenError",
        }
    }
}

export const { handlers, auth, signIn, signOut } = NextAuth({
    pages: {
        signIn: "/account/login",
    },
    // secret: process.env.AUTH_SECRET,
    // trustHost: true,
    debug: process.env.NODE_ENV === "development",
    callbacks: {
        authorized({ auth, request }) {
            const privateRoutes = ["/dashboard"];
            const { pathname } = request.nextUrl;
            const routeName = request.nextUrl.pathname.split("/").slice(0, 2).join("/");

            if (privateRoutes.includes(routeName)) {
                console.log(`${!!auth ? "CAN" : "CANNOT"} access private route ${routeName}`)
                return !!auth;
            } else if (pathname.startsWith("/login") || pathname.startsWith("/forgot-password") || pathname.startsWith("/signup")) {
                const isLoggedIn = !!auth;
                if (isLoggedIn) {
                    return Response.redirect(new URL("/", request.nextUrl));
                }
                return true;
            }
            console.log("AUTHORIZED", auth);
            return true;
        },
        jwt: async ({ token, user, account }) => {
            console.log("JWT\nACCOUNT:", account, "USER:", user, "TOKEN:", token);
            if (user) {
                const accessToken = user.accessToken as String;
                // const user = {
                //     id: token.id,
                //     accessToken: token.accessToken,
                //     refreshToken: token.refreshToken,
                //     role: token.role
                // }
                token.id = user.id;
                token.accessToken = user.accessToken;
                token.refreshToken = user.refreshToken;
                token.role = "Unknown";
                const decodedAccessToken = JSON.parse(Buffer.from(accessToken.split(".")[1], "base64").toString());
                console.log("Decoded: ", decodedAccessToken);

                if (decodedAccessToken) {
                    const username = decodedAccessToken["sub"].split(":")[1];
                    token.username = username as string;
                    token.accessTokenExpires = Date.now() + decodedAccessToken["exp"] * 1000;
                }
                console.log("JWT New Token:", token);
            }
            if ((token.accessTokenExpires && (Date.now() < Number(token.accessTokenExpires))) || token.error == "RefreshAccessTokenError") {
                console.log("VALID TOKEN in JWT");
                token.error = ""

                return token;
            }
            return await refreshAccessToken(token);
        },
        session: async ({ session, token, user }) => {
            console.log("SESSION:", session, "\nUSER:", user, "\nTOKEN:", token);
            return {
                ...session,
                user: {
                    ...session.user,
                    id: token.id as string,
                    email: token.email as string,
                    username: token.username as string,
                    cognitoGroups: token.cognitoGroups as string[],
                    accessToken: token.accessToken as string,
                    accessTokenExpires: token.accessTokenExpires as number,
                    role: token.role as string
                },
                error: ""
            }
        }
    },
    providers: [
        Credentials({
            credentials: {
                username: {},
                password: {},
            },
            authorize: async (credentials) => {
                const myHeaders = new Headers();
                myHeaders.append("Content-Type", "application/x-www-form-urlencoded");

                const urlencoded = new URLSearchParams();
                urlencoded.append("username", "blep");
                urlencoded.append("password", "blepper");

                const requestOptions = {
                    method: "POST",
                    headers: myHeaders,
                    body: urlencoded,
                };

                const response = await fetch(`${process.env.API_BASE_URL}/api/login`, requestOptions)
                    .then((response) => response)
                    .catch((error) => console.error(error));

                if (response) {
                    const data = await response.json();
                    console.log(data);
                    if (data) {
                        const prefix = process.env.NODE_ENV === "development" ? "__Dev-" : "";
                        const cookie = await cookies();

                        cookie.set({
                            name: `MultiCat.refresh-token`,
                            value: data["refresh_token"],
                            httpOnly: true,
                            sameSite: "none",
                            secure: true,
                        });

                        const user = {
                            id: data["id"],
                            cognitoGroups: [],
                            accessToken: data["access_token"],
                            refreshToken: data["refresh_token"],
                            idToken: "",
                            exp: 200,
                            role: ""
                        }

                        return user;
                    }
                }

                return null;
            },
        }),
    ],
});
