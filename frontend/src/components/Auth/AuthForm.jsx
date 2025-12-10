import { useForm } from "react-hook-form";

const AuthForm = ({ isLogin }) => {
    const { register, handleSubmit, formState: { errors } } = useForm();

    const onSubmit = (data) => console.log(data);

    return (
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">

            {!isLogin && (
                <>
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
                                focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 focus:bg-white dark:focus:bg-slate-700
                                transition-all duration-200 outline-none
                            "
                            {...register("name", {
                                required: "Name is required",
                                minLength: { value: 3, message: "Minimum 3 characters" }
                            })}
                        />
                        {errors.name && <p className="text-red-500 text-xs ml-1">{errors.name.message}</p>}
                    </div>
                </>
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
                        focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 focus:bg-white dark:focus:bg-slate-700
                        transition-all duration-200 outline-none
                    "
                    {...register("email", {
                        required: "Email is required",
                    })}
                />
                {errors.email && <p className="text-red-500 text-xs ml-1">{errors.email.message}</p>}
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
                        focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 focus:bg-white dark:focus:bg-slate-700
                        transition-all duration-200 outline-none
                    "
                    {...register("password", {
                        required: "Password is required",
                    })}
                />
                {errors.password && <p className="text-red-500 text-xs ml-1">{errors.password.message}</p>}
            </div>

            {isLogin && (
                <div className="flex justify-end">
                    <button type="button" className="text-sm font-medium text-indigo-600 hover:text-indigo-700 dark:text-indigo-400 dark:hover:text-indigo-300 transition-colors">
                        Forgot Password?
                    </button>
                </div>
            )}

            <button
                type="submit"
                className="
                    w-full py-3.5 rounded-xl 
                    bg-gradient-to-r from-indigo-600 to-violet-600 
                    text-white font-bold tracking-wide
                    hover:from-indigo-700 hover:to-violet-700 
                    hover:shadow-lg hover:-translate-y-px
                    active:translate-y-0
                    transition-all duration-200
                "
            >
                {isLogin ? "Log In" : "Create Account"}
            </button>
        </form>
    );
};

export default AuthForm;
