import { useState } from "react";
import Sources from "../components/Generate/Sources";
import ConfigureQuiz from "../components/Generate/ConfigureQuiz";
import PreviewQuiz from "../components/Generate/PreviewQuiz";

const GenerateQuiz = () => {

    /*
        STATUS: Done
    */

    const [step, setStep] = useState(1);

    return (
        <div className="
            min-h-screen pt-30 pb-12 px-6 
            bg-slate-50 dark:bg-slate-900 
            text-slate-800 dark:text-slate-200
            font-vend
        ">
            <div className="max-w-6xl mx-auto">
                <header className="mb-10 text-center md:text-left">
                    <h1 className="text-4xl font-extrabold font-vend mb-3 text-black dark:text-white">
                        Generate a Quiz
                    </h1>
                    <p className="text-lg text-slate-600 dark:text-slate-400 max-w-2xl">
                        Upload your content, configure the parameters, and let our AI craft the perfect quiz for you in seconds.
                    </p>
                </header>

                <div className="flex items-center gap-4 mb-10 overflow-x-auto pb-4 md:pb-0">
                    <div className={`
                        flex items-center gap-2 px-4 py-2 rounded-full border transition-all duration-300
                        ${step === 1
                            ? "bg-indigo-600 border-indigo-600 text-white shadow-lg shadow-indigo-200 dark:shadow-none"
                            : "bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700 text-slate-500"}
                    `}>
                        <span className="flex items-center justify-center w-6 h-6 rounded-full bg-white/20 text-xs font-bold">1</span>
                        <span className="font-semibold whitespace-nowrap">Resources</span>
                    </div>

                    <div className="w-12 h-0.5 bg-slate-200 dark:bg-slate-700 rounded-full"></div>

                    <div className={`
                        flex items-center gap-2 px-4 py-2 rounded-full border transition-all duration-300
                        ${step === 2
                            ? "bg-indigo-600 border-indigo-600 text-white shadow-lg shadow-indigo-200 dark:shadow-none"
                            : "bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700 text-slate-500"}
                    `}>
                        <span className="flex items-center justify-center w-6 h-6 rounded-full bg-white/20 text-xs font-bold">2</span>
                        <span className="font-semibold whitespace-nowrap">Configuration</span>
                    </div>

                    <div className="w-12 h-0.5 bg-slate-200 dark:bg-slate-700 rounded-full"></div>

                    <div className={`
                        flex items-center gap-2 px-4 py-2 rounded-full border transition-all duration-300
                        ${step === 3
                            ? "bg-indigo-600 border-indigo-600 text-white shadow-lg shadow-indigo-200 dark:shadow-none"
                            : "bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700 text-slate-500"}
                    `}>
                        <span className="flex items-center justify-center w-6 h-6 rounded-full bg-white/20 text-xs font-bold">3</span>
                        <span className="font-semibold whitespace-nowrap">Preview Quiz</span>
                    </div>
                </div>

                <div className="
                    bg-white dark:bg-slate-800 
                    rounded-3xl shadow-sm border border-slate-200 dark:border-slate-700
                    p-6 md:p-8 min-h-[500px]
                ">
                    {step === 1 && <Sources />}
                    {step === 2 && <ConfigureQuiz />}
                    {step === 3 && <PreviewQuiz />}
                </div>

                <div className="flex justify-end mt-8 gap-4">
                    {(step === 2 || step == 3) && (
                        <button
                            onClick={() => setStep(step - 1)}
                            className="px-6 py-3 rounded-xl font-semibold text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700 transition"
                        >
                            Back
                        </button>
                    )}

                    {(step === 1 || step === 2) ? (
                        <button
                            onClick={() => setStep(step + 1)}
                            className="
                                px-8 py-3 rounded-xl font-bold bg-indigo-600 text-white 
                                hover:bg-indigo-700 transition shadow-lg shadow-indigo-200 dark:shadow-none
                            "
                        >
                            Next Step
                        </button>
                    ) : (
                        <button
                            className="
                                px-8 py-3 rounded-xl font-bold bg-green-600 text-white 
                                hover:bg-green-700 transition shadow-lg shadow-green-200 dark:shadow-none
                            "
                        >
                            Generate Quiz
                        </button>
                    )}
                </div>
            </div>
        </div>
    );
};

export default GenerateQuiz;