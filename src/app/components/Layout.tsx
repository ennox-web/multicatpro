
import Menu from "../ui/menu/menu";
import SessionProviderWrapper from "./SessionProviderWrapper";

export default function Layout({ children }: { children: React.ReactNode }) {
    return (
        <div>
            <SessionProviderWrapper>
                <div>
                    <Menu />
                </div>
                <div>{children}</div>
            </SessionProviderWrapper>
        </div>
    );
}
