import { useEffect, useState } from "react";
import { Settings, Clock, Hash, Layers, CheckSquare, ListChecks } from "lucide-react";

/*
    TODO: Add tags data
    TODO: Make difficulty and question types functional
    TODO: Make Question count better
*/

export default function ConfigureQuiz() {

    const marks = Array.from({ length: 10 }, (_, i) => 5 + i * 5)
    const [difficulty, setDifficulty] = useState("Easy")
    const [questionType, setQuestionType] = useState([])
    const [live, setLive] = useState(false)
    const [leaderboard, setLeaderboard] = useState(false)

    const QUESTION_TYPES = [
        { label: "Single correct (SCQ)", value: "scq" },
        { label: "Multiple correct (MCQ)", value: "mcq" },
        { label: "True / False", value: "tfq" },
        { label: "Fill in the Blanks", value: "fib" },
    ]
    const toggleQuestionType = (type) => {
        setQuestionType((prev) =>
            prev.includes(type)
                ? prev.filter((t) => t !== type)
                : [...prev, type]
        )
    }

    return (
        <div className="flex flex-col gap-8">
            {/* Header */}
            <div className="flex items-center gap-3 pb-4 border-b border-slate-200 dark:border-slate-700">
                <div className="w-10 h-10 rounded-xl bg-indigo-100 dark:bg-indigo-900/30 flex items-center justify-center text-indigo-600 dark:text-indigo-400">
                    <Settings size={22} />
                </div>
                <div>
                    <h2 className="text-xl font-bold text-slate-800 dark:text-slate-100">Quiz Configuration</h2>
                    <p className="text-sm text-slate-500 dark:text-slate-400">Customize your quiz parameters</p>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-8">
                {/* Question Count */}
                <div className="space-y-3">
                    <label className="flex items-center gap-2 text-sm font-bold text-slate-700 dark:text-slate-300">
                        <Hash size={16} /> Number of Questions
                    </label>

                    <div className="flex flex-col w-full">
                        <input
                            type="range"
                            min="5"
                            max="50"
                            step="5"
                            defaultValue="10"
                            className="
                        w-full h-2 appearance-none rounded-lg cursor-pointer
                        bg-slate-200 dark:bg-slate-700
                        accent-indigo-600
                        "
                        />

                        <div className="mt-4 z-50 w-full flex justify-between text-xs text-slate-500 font-medium">
                            {marks.map((mark) => (
                                <span key={mark}>{mark}</span>
                            ))}
                        </div>
                    </div>
                </div>
                {/* Difficulty Settings */}
                <div className="space-y-3">
                    <label className="flex items-center gap-2 text-sm font-bold text-slate-700 dark:text-slate-300">
                        <Layers size={16} /> Difficulty Level
                    </label>
                    <div className="flex p-1 bg-slate-100 dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-700/50">
                        {['Easy', 'Medium', 'Hard'].map((level, idx) => (
                            <button
                                key={level}
                                className={`
                                    flex-1 py-2 rounded-lg text-sm font-bold transition-all
                                    ${level === difficulty
                                        ? "bg-white dark:bg-slate-700 text-indigo-600 dark:text-indigo-400 shadow-sm"
                                        : "text-slate-500 hover:text-slate-700 dark:hover:text-slate-300"}
                                `}
                                onClick={() => setDifficulty(level)}
                            >
                                {level}
                            </button>
                        ))}
                    </div>
                </div>

                {/* Time Limit */}
                <div className="space-y-3">
                    <label className="flex items-center gap-2 text-sm font-bold text-slate-700 dark:text-slate-300">
                        <Clock size={16} /> Time Limit of Exam(in Minutes)
                    </label>
                    <input
                        type="number"
                        className="
                        w-full p-3 rounded-xl 
                        bg-slate-50 dark:bg-slate-900 
                        border border-slate-200 dark:border-slate-700
                        text-slate-800 dark:text-slate-200
                        focus:ring-2 focus:ring-indigo-500 outline-none
                        appearance-none
                        "
                    />
                    <label className="flex items-center gap-2 text-sm font-bold text-slate-700 dark:text-slate-300">
                        <Clock size={16} /> Start time of Exam(in 24Hr format)
                    </label>
                    <input
                        type="time"
                        className="
                        w-full p-3 rounded-xl 
                        bg-slate-50 dark:bg-slate-900 
                        border border-slate-200 dark:border-slate-700
                        text-slate-800 dark:text-slate-200
                        focus:ring-2 focus:ring-indigo-500 outline-none
                        appearance-none"
                    />
                </div>

                {/* Question Types */}
                <div className="space-y-3">
                    <label className="flex items-center gap-2 text-sm font-bold text-slate-700 dark:text-slate-300">
                        <ListChecks size={16} /> Question Types
                    </label>

                    <div className="grid grid-cols-1 gap-2">
                        {QUESTION_TYPES.map(({ label, value }) => (
                            <ToggleOption
                                key={value}
                                label={label}
                                active={questionType.includes(value)}
                                onClick={() => toggleQuestionType(value)}
                            />
                        ))}
                    </div>
                </div>


            </div>

            {/* Extra Options */}
            <div className="pt-6 border-t border-slate-200 dark:border-slate-700 grid grid-cols-1 md:grid-cols-2 gap-6">
                <ToggleSwitch
                    label="Host Live Quiz"
                    desc="Start a real-time session for others to join"
                    item={live}
                    setItem={setLive}
                />
                <ToggleSwitch
                    label="Show Leaderboard"
                    desc="Display rankings after each question"
                    item={leaderboard}
                    setItem={setLeaderboard}
                />
            </div>
        </div>
    );
}

function ToggleOption({ label, active, onClick }) {
    return (
        <div
            onClick={onClick}
            className={`
        flex items-center justify-between p-3 rounded-xl border cursor-pointer transition-all
        ${active
                    ? "bg-indigo-50 dark:bg-indigo-900/10 border-indigo-200 dark:border-indigo-500/30 text-indigo-700 dark:text-indigo-300"
                    : "bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700 text-slate-500"}
      `}
        >
            <span className="text-sm font-semibold">{label}</span>

            <div
                className={`
          w-5 h-5 rounded flex items-center justify-center border
          ${active
                        ? "bg-indigo-600 border-indigo-600 text-white"
                        : "border-slate-300 dark:border-slate-600"}
        `}
            >
                {active && <CheckSquare size={14} />}
            </div>
        </div>
    )
}


function ToggleSwitch({ label, desc, item, setItem }) {
    return (
        <div className="flex items-center justify-between">
            <div className="flex-1">
                <p className="font-bold text-slate-800 dark:text-slate-200">{label}</p>
                <p className="text-xs text-slate-500">{desc}</p>
            </div>
            <div className={`
                w-12 h-6 rounded-full p-1 transition-colors duration-300 cursor-pointer
                ${item ? "bg-indigo-600" : "bg-slate-200 dark:bg-slate-700"}
            `}
                onClick={() => setItem((prev) => !prev)}
            >
                <div className={`
                    w-4 h-4 rounded-full bg-white shadow-sm transition-transform duration-300
                    ${item ? "translate-x-6" : "translate-x-0"}
                `}></div>
            </div>
        </div>
    )
}
