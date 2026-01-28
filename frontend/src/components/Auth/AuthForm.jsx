import { useForm } from "react-hook-form";
import axios from "axios";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";

export default function AuthForm({ isLogin }) {
    const {
        register,
        handleSubmit,
        formState: { errors, isSubmitting },
    } = useForm();

    const navigate = useNavigate();

    const onSubmit = async (data) => {
        try {
            const backend_url =
                import.meta.env.VITE_BACKEND_URL +
                (isLogin ? "/auth/login" : "/auth/register");

            const response = await axios.post(backend_url, data);
            if (isLogin) {
                toast.success(response.data.message);
                navigate("/dashboard");
            }
            else {
                toast.success(response.data.message);
                toast.info("Please login to continue");
                navigate("/login");
            }
        } catch (error) {
            toast.error(error?.response?.data?.detail || "Something went wrong");
        }
    };

    return (
        <form
            onSubmit={handleSubmit(onSubmit)}
            className="space-y-5"
            noValidate
        >
            {!isLogin && (
                <div className="space-y-1">
                    <input
                        type="text"
                        placeholder="Name"
                        className="
                            w-full p-3.5 rounded-xl 
                            bg-slate-50 dark:bg-slate-700/50
                            border border-slate-200 dark:border-slate-600
                            text-slate-900 dark:text-slate-200
                            placeholder-slate-400 dark:placeholder-slate-500
                            focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500
                            transition-all duration-200 outline-none
                        "
                        {...register("username", {
                            required: "Name is required",
                            minLength: {
                                value: 3,
                                message: "Minimum 3 characters",
                            },
                        })}
                    />
                    {errors.username && (
                        <p className="text-red-500 text-xs ml-1">
                            {errors.username.message}
                        </p>
                    )}
                </div>
            )}

            <div className="space-y-1">
                <input
                    type="email"
                    placeholder="Email"
                    className="
                        w-full p-3.5 rounded-xl 
                        bg-slate-50 dark:bg-slate-700/50
                        border border-slate-200 dark:border-slate-600
                        text-slate-900 dark:text-slate-200
                        placeholder-slate-400 dark:placeholder-slate-500
                        focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500
                        transition-all duration-200 outline-none
                    "
                    {...register("email", {
                        required: "Email is required",
                    })}
                />
                {errors.email && (
                    <p className="text-red-500 text-xs ml-1">
                        {errors.email.message}
                    </p>
                )}
            </div>

            <div className="space-y-1">
                <input
                    type="password"
                    placeholder="Password"
                    className="
                        w-full p-3.5 rounded-xl 
                        bg-slate-50 dark:bg-slate-700/50
                        border border-slate-200 dark:border-slate-600
                        text-slate-900 dark:text-slate-200
                        placeholder-slate-400 dark:placeholder-slate-500
                        focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500
                        transition-all duration-200 outline-none
                    "
                    {...register("password", {
                        required: "Password is required",
                    })}
                />
                {errors.password && (
                    <p className="text-red-500 text-xs ml-1">
                        {errors.password.message}
                    </p>
                )}
            </div>

            {isLogin && (
                <div className="flex justify-end">
                    <button
                        type="button"
                        className="text-sm font-medium text-indigo-600 hover:text-indigo-700 transition-colors"
                    >
                        Forgot Password?
                    </button>
                </div>
            )}

            <button
                type="submit"
                disabled={isSubmitting}
                className="
                    w-full py-3.5 rounded-xl 
                    bg-blue-700
                    text-white font-bold tracking-wide
                    flex items-center justify-center gap-2
                    hover:bg-blue-600
                    hover:shadow-lg hover:-translate-y-px
                    transition-all duration-200
                    disabled:opacity-70 disabled:cursor-not-allowed
                "
            >
                {isSubmitting ? (
                    <>
                        <span className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                        <span>{isLogin ? "Logging in..." : "Creating..."}</span>
                    </>
                ) : (
                    isLogin ? "Log In" : "Create Account"
                )}
            </button>
        </form>
    );
}
