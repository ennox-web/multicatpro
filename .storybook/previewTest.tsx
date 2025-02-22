import type { Preview } from "@storybook/react";
import React from "react";
import { SessionProvider } from "next-auth/react";

import '../src/app/globals.css';
import { roboto } from '../src/app/lib/fonts';

const previewTest: Preview = {
    parameters: {
        controls: {
            matchers: {
                color: /(background|color)$/i,
                date: /Date$/i,
            },
        },
        nextjs: {
            appDirectory: true,
        }
    },
    decorators: [
        (Story, context) => {
            const session = context.globals.mockSession ? {
                expires: "",
                user: {
                    id: "1",
                    email: "blep@blep.com",
                    username: "blep",
                    cognitoGroups: [],
                    accessToken: "asdf",
                    accessTokenExpires: 987654321,
                    refreshToken: "fdsa",
                    idToken: "",
                    exp: 123456789,
                    role: "Unknown"
                },
                error: "",
            } : null;

            return (
                <SessionProvider>
                    <div className={`${roboto.className}`}>
                        <Story />
                    </div>
                </SessionProvider>
            );
        },
    ],
    globalTypes: {
        mockSession: {
            name: 'Mock Session',
            description: 'Enable/disable mock session',
            defaultValue: false,
            toolbar: {
              icon: 'user',
              items: [{ value: true, title: 'Logged In' }, { value: false, title: 'Logged Out' }],
              title: 'User State',
              dynamicTitle: true,
            },
        },
    },
};

export default previewTest;
