import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import Sources from "../components/Generate/Sources";
import ConfigureQuiz from "../components/Generate/ConfigureQuiz";
import PreviewQuiz from "../components/Generate/PreviewQuiz";
import api from "../utils/api";

const GenerateQuiz = () => {
    const navigate = useNavigate();
    const [step, setStep] = useState(1);
    const [quizId, setQuizId] = useState(null);
    const [generating, setGenerating] = useState(false);
    const [publishing, setPublishing] = useState(false);
    const [questions, setQuestions] = useState([]);
    
    // Lifted state for sources
    const [files, setFiles] = useState([]);
    const [urls, setUrls] = useState([]);
    
    const [config, setConfig] = useState({
        quiz_name: "",
        question_count: 10,
        quiz_difficulty: "MEDIUM",
        quiz_start_time: "",
        quiz_duration: 15,
        show_leaderboard: true,
        question_types: ["scq", "mcq"]
    });

    const handleNext = async () => {
        if (step === 1) {
            // Validate configuration
            if (!config.quiz_name.trim()) {
                toast.error("Please enter a quiz name");
                return;
            }
            if (!config.quiz_start_time) {
                toast.error("Please select a start date and time");
                return;
            }
            if (config.question_types.length === 0) {
                toast.error("Please select at least one question type");
                return;
            }

            try {
                // Format payload. Map Difficulty to uppercase enum
                const payload = {
                    quiz_name: config.quiz_name,
                    question_count: parseInt(config.question_count),
                    quiz_difficulty: config.quiz_difficulty.toUpperCase(),
                    quiz_start_time: new Date(config.quiz_start_time).toISOString(),
                    quiz_duration: parseInt(config.quiz_duration),
                    show_leaderboard: config.show_leaderboard,
                    status: "draft"
                };

                if (quizId) {
                    await api.put("/quizes/update", { ...payload, quiz_id: quizId });
                } else {
                    const res = await api.post("/quizes/create", payload);
                    setQuizId(res.data.quiz_id || res.data.id);
                }
                setStep(2);
            } catch (err) {
                console.error(err);
                toast.error("Failed to save quiz configuration");
            }
        } else if (step === 2) {
            setStep(3);
        }
    };

    const handleGenerate = async () => {
        if (!quizId) return;
        setGenerating(true);
        try {
            const res = await api.post(`/quizes/${quizId}/generate`);
            setQuestions(res.data);
            toast.success("AI generated questions successfully!");
        } catch (err) {
            console.error(err);
            toast.error("Failed to generate questions. Ensure you have uploaded resources first.");
        } finally {
            setGenerating(false);
        }
    };

    const handlePublish = async () => {
        if (!quizId) return;
        setPublishing(true);
        try {
            await api.post(`/quizes/${quizId}/publish`);
            toast.success("Quiz published successfully!");
            navigate("/host");
        } catch (err) {
            console.error(err);
            toast.error("Failed to publish quiz");
        } finally {
            setPublishing(false);
        }
    };

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
                        Configure the parameters, upload your content, and let our AI craft the perfect quiz for you in seconds.
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
                        <span className="font-semibold whitespace-nowrap">Configuration</span>
                    </div>

                    <div className="w-12 h-0.5 bg-slate-200 dark:bg-slate-700 rounded-full"></div>

                    <div className={`
                        flex items-center gap-2 px-4 py-2 rounded-full border transition-all duration-300
                        ${step === 2
                            ? "bg-indigo-600 border-indigo-600 text-white shadow-lg shadow-indigo-200 dark:shadow-none"
                            : "bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700 text-slate-500"}
                    `}>
                        <span className="flex items-center justify-center w-6 h-6 rounded-full bg-white/20 text-xs font-bold">2</span>
                        <span className="font-semibold whitespace-nowrap">Resources</span>
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
                    {step === 1 && <ConfigureQuiz config={config} setConfig={setConfig} />}
                    {step === 2 && <Sources quizId={quizId} files={files} setFiles={setFiles} urls={urls} setUrls={setUrls} />}
                    {step === 3 && (
                        <PreviewQuiz 
                            quizId={quizId} 
                            questions={questions} 
                            onGenerate={handleGenerate} 
                            generating={generating} 
                        />
                    )}
                </div>

                <div className="flex justify-end mt-8 gap-4">
                    {step > 1 && (
                        <button
                            onClick={() => setStep(step - 1)}
                            className="px-6 py-3 rounded-xl font-semibold text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700 transition"
                        >
                            Back
                        </button>
                    )}

                    {step < 3 ? (
                        <button
                            onClick={handleNext}
                            className="
                                px-8 py-3 rounded-xl font-bold bg-indigo-600 text-white 
                                hover:bg-indigo-700 transition shadow-lg shadow-indigo-200 dark:shadow-none
                            "
                        >
                            Next Step
                        </button>
                    ) : (
                        <button
                            onClick={handlePublish}
                            disabled={questions.length === 0 || publishing}
                            className="
                                px-8 py-3 rounded-xl font-bold bg-green-600 text-white 
                                hover:bg-green-700 transition shadow-lg shadow-green-200 dark:shadow-none
                                disabled:opacity-50 disabled:cursor-not-allowed
                            "
                        >
                            {publishing ? "Publishing..." : "Publish Quiz"}
                        </button>
                    )}
                </div>
            </div>
        </div>
    );
};

export default GenerateQuiz;