import { auth } from '@/auth';
import { NextResponse } from 'next/server';

// export {auth as middleware} from "./auth";

export default auth((req) => {
    console.log("IN MIDDLEWARE?");
    return NextResponse.next();
})

export const config = {
    matcher: ['/((?!api|_next/static|_next/image|favicon.ico|sitemap.xml|robots.txt).*)']
};
