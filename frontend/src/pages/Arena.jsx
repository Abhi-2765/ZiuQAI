import { Timer, ArrowLeft, ArrowRight, EllipsisVertical, StepForward, BookmarkPlus } from "lucide-react";
import { useState } from "react";
import ThemeChanger from "../components/common/ThemeChanger";
import Question from "../components/Arena/Question";
import Navigation from "../components/Arena/Navigation";

export default function Arena() {
    const [time, setTime] = useState(120);
    const [questionIndex, setQuestionIndex] = useState(0);
    const [totalQuestions] = useState(15);

    const [questions, setQuestions] = useState([{
        question: "What is the capital of France?",
        type: "scq",
        options: ["True", "False"]
    }]);

    return (
        <div className="
            w-full min-h-screen px-4 md:px-16 py-8
            bg-slate-50 dark:bg-slate-900 
            text-slate-800 dark:text-slate-100 
            font-vend
        "
        >
            <section className="
                flex justify-between items-center 
                mb-10
            ">
                <div className="
                    text-lg font-semibold border-2 border-violet-600 
                    px-4 py-2 rounded-xl
                ">
                    {questionIndex} / {totalQuestions}
                </div>

                <div className="flex items-center gap-4">
                    <div className="
                        flex items-center gap-2 mx-4 px-4 py-2 
                        border-2 border-violet-600 rounded-xl
                        text-violet-600 dark:text-violet-400
                    ">
                        <Timer />
                        {time}
                    </div>

                    <ThemeChanger />

                    <button className="
                        p-2 rounded-xl 
                        bg-white dark:bg-slate-800 
                        border border-slate-300 dark:border-slate-700
                    "
                        onClick={() => { }}
                    >
                        <EllipsisVertical className="w-5 h-5" />
                    </button>
                </div>
            </section >

            <section className="max-w-3xl mx-auto mt-10">
                <Question question={questions[questionIndex]} />
                <ActionBtn icon={<BookmarkPlus />} text="Mark for Review" />
                <ActionBtn icon={<StepForward />} text="Save and Next" />
            </section>

            <section className="flex justify-center gap-6 mt-16">
                <NavBtn icon={<ArrowLeft />} />
                <NavBtn icon={<ArrowRight />} />
            </section>

            <Navigation questions={questions} />
        </div >
    );
}

const ActionBtn = ({ icon, text }) => {
    const isReview = text === "Mark for Review";

    const baseStyles =
        "px-4 py-2 rounded-xl flex items-center gap-2 transition font-medium shadow-sm";

    const variant = isReview
        ? `
        border border-violet-600 text-violet-600
        dark:text-violet-400 dark:border-violet-400
        hover:bg-violet-600 hover:text-white
        dark:hover:bg-violet-500 dark:hover:text-white
        `
        : `
        border border-green-600 text-green-600
        dark:text-green-400 dark:border-green-400
        hover:bg-green-600 hover:text-white
        dark:hover:bg-green-500 dark:hover:text-white
        `;

    return (
        <div className="flex justify-end mt-6">
            <button className={`${baseStyles} ${variant}`}>
                {icon}
                {text}
            </button>
        </div>
    );
};

const NavBtn = ({ icon }) => {
    return (
        <button className="
            rounded-full p-3 border-2 border-violet-600
            text-violet-600 dark:text-violet-400
            hover:bg-violet-600 hover:text-white
            transition
        ">
            {icon}
        </button>
    )
}