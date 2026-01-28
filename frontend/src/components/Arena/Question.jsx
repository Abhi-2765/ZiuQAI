import { BookmarkPlus } from "lucide-react";

const defaultQuestion = {
    question: "Hi",
    type: "tfq", // fib | scq | mcq | tfq
    options: ["True", "False"],
};

export default function Question({ question = defaultQuestion }) {
    const { question: text, type, options = [] } = question;

    return (
        <div>
            <p className="text-2xl font-bold mb-6">
                {text}
            </p>

            {/* Fill in the blank */}
            {type === "fib" ? (
                <div className="mt-6">
                    <input
                        type="number"
                        id={text}
                        className="
                            w-full px-4 py-3 rounded-xl 
                            bg-white dark:bg-slate-800
                            border border-slate-300 dark:border-slate-700
                            focus:ring-2 focus:ring-violet-600 
                            outline-none
                        "
                    />
                    <label
                        htmlFor={text}
                        className="text-sm text-slate-600 dark:text-slate-400 mt-2 block"
                    >
                        Enter numerical value
                    </label>
                </div>
            ) : (
                <div className="flex flex-col gap-4 mt-4">
                    {options.map((option, index) => (
                        <Option
                            key={index}
                            option={option}
                            type={type}
                            name={text} // 👈 important for radio grouping
                        />
                    ))}
                </div>
            )}
        </div>
    );
}

const Option = ({ option, type, name }) => {
    const inputType = type === "scq" || type === "tfq" ? "radio" : "checkbox";

    return (
        <label
            className="
                w-full p-4 rounded-xl cursor-pointer
                bg-white dark:bg-slate-800 
                border border-slate-300 dark:border-slate-700
                hover:border-violet-600 
                flex gap-3 items-center
                transition shadow-sm
            "
        >
            <input
                type={inputType}
                name={name}
                value={option}
                className="w-5 h-5 accent-violet-600"
            />
            <span className="text-lg">{option}</span>
        </label>
    );
};
