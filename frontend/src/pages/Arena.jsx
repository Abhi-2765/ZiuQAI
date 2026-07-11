import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import { Timer, ArrowLeft, ArrowRight, CheckCircle2, BookmarkPlus, AlertTriangle } from "lucide-react";
import ThemeChanger from "../components/common/ThemeChanger";
import Question from "../components/Arena/Question";
import Navigation from "../components/Arena/Navigation";
import api from "../utils/api";

export default function Arena() {
    const { quizId } = useParams();
    const navigate = useNavigate();

    const [loading, setLoading] = useState(true);
    const [questions, setQuestions] = useState([]);
    const [answers, setAnswers] = useState({}); // { qid: answer_string }
    const [statuses, setStatuses] = useState({}); // { index: "notVisited" | "complete" | "markForReview" }
    const [questionIndex, setQuestionIndex] = useState(0);
    const [time, setTime] = useState(0); // in seconds
    const [submitting, setSubmitting] = useState(false);

    // Fetch questions and details
    useEffect(() => {
        const loadQuizData = async () => {
            try {
                // Get details for duration
                const detailsRes = await api.get(`/quizes/${quizId}`);
                const duration = detailsRes.data.quiz_duration * 60;
                
                // Get questions
                const qRes = await api.get(`/quizes/${quizId}/attempt/questions`);
                setQuestions(qRes.data);
                
                // Initialize state
                setTime(duration);
                const initialStatuses = {};
                qRes.data.forEach((_, idx) => {
                    initialStatuses[idx] = idx === 0 ? "current" : "notVisited";
                });
                setStatuses(initialStatuses);
            } catch (err) {
                console.error(err);
                toast.error("Failed to load quiz attempt");
                navigate("/attempt");
            } finally {
                setLoading(false);
            }
        };
        loadQuizData();
    }, [quizId]);

    // Timer countdown
    useEffect(() => {
        if (loading || time <= 0) {
            if (time === 0 && !loading && questions.length > 0) {
                handleSubmit(true); // Auto submit on timeout
            }
            return;
        }

        const timer = setInterval(() => {
            setTime((prev) => prev - 1);
        }, 1000);

        return () => clearInterval(timer);
    }, [time, loading]);

    const formatTime = (totalSeconds) => {
        const m = Math.floor(totalSeconds / 60);
        const s = totalSeconds % 60;
        return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
    };

    const handleAnswerChange = (answer) => {
        const currentQ = questions[questionIndex];
        if (!currentQ) return;
        setAnswers({ ...answers, [currentQ.id]: answer });
    };

    const handleMarkReview = () => {
        setStatuses({ ...statuses, [questionIndex]: "markForReview" });
        handleNext();
    };

    const handleSaveNext = () => {
        const currentQ = questions[questionIndex];
        if (answers[currentQ.id]) {
            setStatuses({ ...statuses, [questionIndex]: "complete" });
        } else {
            setStatuses({ ...statuses, [questionIndex]: "current" }); // marked as not attempted (red/current)
        }
        handleNext();
    };

    const handleNext = () => {
        if (questionIndex < questions.length - 1) {
            const nextIdx = questionIndex + 1;
            setQuestionIndex(nextIdx);
            // Mark next as current if it was notVisited
            if (statuses[nextIdx] === "notVisited") {
                setStatuses({ ...statuses, [questionIndex]: statuses[questionIndex] === "notVisited" ? "current" : statuses[questionIndex], [nextIdx]: "current" });
            }
        }
    };

    const handlePrev = () => {
        if (questionIndex > 0) {
            setQuestionIndex(questionIndex - 1);
        }
    };

    const handleSelectQuestion = (idx) => {
        setQuestionIndex(idx);
        if (statuses[idx] === "notVisited") {
            setStatuses({ ...statuses, [idx]: "current" });
        }
    };

    const handleSubmit = async (auto = false) => {
        if (!auto && !window.confirm("Are you sure you want to submit your quiz attempt?")) return;
        
        setSubmitting(true);
        try {
            await api.post(`/quizes/${quizId}/attempt/submit`, { responses: answers });
            toast.success("Quiz submitted successfully!");
            navigate(`/standings/${quizId}`);
        } catch (err) {
            console.error(err);
            toast.error("Failed to submit quiz responses");
        } finally {
            setSubmitting(false);
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-slate-50 dark:bg-slate-900 flex items-center justify-center">
                <div className="w-10 h-10 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin"></div>
            </div>
        );
    }

    if (questions.length === 0) {
        return (
            <div className="min-h-screen bg-slate-50 dark:bg-slate-900 flex flex-col items-center justify-center p-6 text-center">
                <AlertTriangle className="w-16 h-16 text-amber-500 mb-4 animate-bounce" />
                <h3 className="text-xl font-bold mb-2">No Questions Found</h3>
                <p className="text-slate-500 mb-6">This quiz has no questions generated yet.</p>
                <button onClick={() => navigate("/attempt")} className="px-6 py-2 bg-indigo-600 text-white rounded-xl">Go Back</button>
            </div>
        );
    }

    const currentQ = questions[questionIndex];

    return (
        <div className="
            w-full min-h-screen px-4 md:px-16 py-8
            bg-slate-50 dark:bg-slate-900 
            text-slate-800 dark:text-slate-100 
            font-vend
        ">
            {/* Header */}
            <section className="flex justify-between items-center mb-10">
                <div className="
                    text-lg font-bold border-2 border-violet-600 
                    px-4 py-2 rounded-xl text-violet-600 dark:text-violet-400
                ">
                    Question {questionIndex + 1} / {questions.length}
                </div>

                <div className="flex items-center gap-4">
                    <div className={`
                        flex items-center gap-2 px-4 py-2 
                        border-2 rounded-xl font-bold font-mono
                        ${time < 60 ? "border-red-500 text-red-500 animate-pulse" : "border-violet-600 text-violet-600 dark:text-violet-400"}
                    `}>
                        <Timer size={18} />
                        {formatTime(time)}
                    </div>

                    <ThemeChanger />

                    <button
                        onClick={() => handleSubmit()}
                        disabled={submitting}
                        className="
                            px-6 py-2 bg-green-600 hover:bg-green-700 disabled:opacity-50 text-white font-bold rounded-xl transition
                            flex items-center gap-2 shadow-sm
                        "
                    >
                        <CheckCircle2 size={16} />
                        {submitting ? "Submitting..." : "Submit Quiz"}
                    </button>
                </div>
            </section>

            {/* Main Layout: Question + Navigator */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 max-w-6xl mx-auto items-start">
                <div className="lg:col-span-8 bg-white dark:bg-slate-800 rounded-3xl p-6 md:p-8 border border-slate-200 dark:border-slate-700 shadow-sm">
                    <Question
                        question={currentQ}
                        selectedAnswer={answers[currentQ.id]}
                        onAnswerChange={handleAnswerChange}
                    />

                    <div className="flex flex-wrap gap-4 justify-between mt-12 pt-6 border-t border-slate-100 dark:border-slate-700">
                        <button
                            onClick={handleMarkReview}
                            className="
                                px-5 py-2.5 rounded-xl border border-violet-600 text-violet-600
                                dark:text-violet-400 dark:border-violet-400
                                hover:bg-violet-600 hover:text-white transition font-bold flex items-center gap-2 text-sm
                            "
                        >
                            <BookmarkPlus size={16} />
                            Mark for Review
                        </button>
                        <button
                            onClick={handleSaveNext}
                            className="
                                px-6 py-2.5 rounded-xl bg-violet-600 hover:bg-violet-700 text-white transition
                                font-bold flex items-center gap-2 text-sm shadow-sm
                            "
                        >
                            Save and Next
                        </button>
                    </div>
                </div>

                <div className="lg:col-span-4 flex justify-center lg:justify-end">
                    <Navigation
                        questions={questions}
                        statuses={statuses}
                        currentIndex={questionIndex}
                        onSelect={handleSelectQuestion}
                    />
                </div>
            </div>

            {/* Navigation buttons at bottom */}
            <section className="flex justify-center gap-6 mt-12 pb-10">
                <button
                    onClick={handlePrev}
                    disabled={questionIndex === 0}
                    className="
                        rounded-full p-3 border-2 border-violet-600 text-violet-600 dark:text-violet-400
                        hover:bg-violet-600 hover:text-white transition disabled:opacity-30 disabled:cursor-not-allowed
                    "
                >
                    <ArrowLeft size={20} />
                </button>
                <button
                    onClick={handleNext}
                    disabled={questionIndex === questions.length - 1}
                    className="
                        rounded-full p-3 border-2 border-violet-600 text-violet-600 dark:text-violet-400
                        hover:bg-violet-600 hover:text-white transition disabled:opacity-30 disabled:cursor-not-allowed
                    "
                >
                    <ArrowRight size={20} />
                </button>
            </section>
        </div>
    );
}