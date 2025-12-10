import google from "../../assets/google.png";

const Others = () => {
    return (
        <button
            className="
                w-full flex items-center justify-center gap-3 
                bg-white dark:bg-slate-700
                border border-slate-300 dark:border-slate-600
                text-slate-700 dark:text-slate-200
                py-3 rounded-xl 
                hover:bg-slate-100 dark:hover:bg-slate-600 
                transition
            "
        >
            <img src={google} alt="Google" className="w-5 h-5" />
            Continue with Google
        </button>
    );
};

export default Others;
