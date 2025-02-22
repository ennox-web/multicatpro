import type { Metadata } from "next";
import "./globals.css";

import { roboto } from './lib/fonts';

import Layout from "./components/Layout";

export const metadata: Metadata = {
    title: "MultiCatPro",
    description: "Multi-Categorized Projects",
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
            <body className={roboto.className}>
                <Layout> {children} </Layout>
            </body>
        </html>
    );
}
