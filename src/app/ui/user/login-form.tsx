"use client";

// import { useActionState } from "react";
import { useFormState } from "react-dom";
import { authenticate } from "@/app/lib/actions";
// import { signIn } from "@/auth";


export default function LoginForm() {
    // const [state, formAction, isPending] = useFormState(
    //     authenticate,
    //     initialState,
    // );
    // const [errorMessage, formAction, isPending] = useFormState(
    //     authenticate,
    //     undefined,
    // );

    return (
        <form action={() => {authenticate}}>
            <div>
                <h1>
                    Please log in to continue.
                </h1>
                <div>
                    <div>
                        <label
                            htmlFor="email"
                        >
                            Email
                        </label>
                        <div>
                            <input
                                id="username"
                                type="username"
                                name="username"
                                placeholder="Enter your username"
                                required
                            />
                        </div>
                        <div className="mt-4">
                            <label
                                htmlFor="password"
                            >
                                Password
                            </label>
                            <div className="relative">
                                <input
                                    id="password"
                                    type="password"
                                    name="password"
                                    placeholder="Enter password"
                                    required
                                    minLength={6}
                                />
                            </div>
                        </div>
                        {/* <input type="hidden" name="redirectTo" value={callbackUrl} /> */}
                        {/* <button aria-disabled={isPending}>Login</button> */}
                        <button>Login</button>
                    </div>
                </div>
            </div>
        </form >
    );
}





//                 {/* <Button className="mt-4 w-full" aria-disabled={isPending}>
//           Log in <ArrowRightIcon className="ml-auto h-5 w-5 text-gray-50" />
//         </Button> */}
