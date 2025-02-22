"use client";

import { SessionProvider } from "next-auth/react";

export default function SessionProviderWrapper({ children }: { children: any }) {
    return <SessionProvider>{children}</SessionProvider>;
}
