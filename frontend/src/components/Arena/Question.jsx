import { Check } from "lucide-react";

const defaultQuestion = {
    question: "Default Question Text?",
    type: "tof",
    options: ["True", "False"],
};

export default function Question({ question = defaultQuestion, selectedAnswer, onAnswerChange }) {
    const { question: text, type, options = [] } = question;

    const handleFibChange = (e) => {
        if (onAnswerChange) {
            onAnswerChange(e.target.value);
        }
    };

    const handleOptionSelect = (option) => {
        if (!onAnswerChange) return;

        if (type === "scq" || type === "tof" || type === "tfq") {
            onAnswerChange(option);
        } else if (type === "mcq") {
            // Multiple Choice: selectedAnswer is comma-separated string or array
            const currentSelected = selectedAnswer ? selectedAnswer.split(", ") : [];
            let updated;
            if (currentSelected.includes(option)) {
                updated = currentSelected.filter((item) => item !== option);
            } else {
                updated = [...currentSelected, option];
            }
            onAnswerChange(updated.join(", "));
        }
    };

    return (
        <div>
            <p className="text-xl font-bold mb-6 text-slate-800 dark:text-slate-100">
                {text}
            </p>

            {type === "fib" ? (
                <div className="mt-6">
                    <input
                        type="text"
                        placeholder="Enter your answer"
                        value={selectedAnswer || ""}
                        onChange={handleFibChange}
                        className="
                            w-full px-4 py-3 rounded-xl 
                            bg-white dark:bg-slate-800
                            border border-slate-300 dark:border-slate-700
                            focus:ring-2 focus:ring-violet-600 
                            outline-none text-slate-800 dark:text-slate-100
                        "
                    />
                </div>
            ) : (
                <div className="flex flex-col gap-4 mt-4">
                    {options.map((option, index) => {
                        const isSelected = type === "mcq"
                            ? (selectedAnswer ? selectedAnswer.split(", ").includes(option) : false)
                            : (selectedAnswer === option);
                        
                        return (
                            <div
                                key={index}
                                onClick={() => handleOptionSelect(option)}
                                className={`
                                    w-full p-4 rounded-xl cursor-pointer
                                    bg-white dark:bg-slate-800 border transition shadow-sm
                                    flex gap-3 items-center
                                    ${isSelected 
                                        ? "border-violet-600 bg-violet-50/50 dark:bg-violet-950/20" 
                                        : "border-slate-300 dark:border-slate-700 hover:border-violet-600/50"}
                                `}
                            >
                                <div className={`
                                    w-5 h-5 rounded-full border flex items-center justify-center
                                    ${isSelected 
                                        ? "bg-violet-600 border-violet-600 text-white" 
                                        : "border-slate-300 dark:border-slate-600"}
                                `}>
                                    {isSelected && <Check size={12} strokeWidth={3} />}
                                </div>
                                <span className="text-lg text-slate-700 dark:text-slate-200">{option}</span>
                            </div>
                        );
                    })}
                </div>
            )}
        </div>
    );
}
