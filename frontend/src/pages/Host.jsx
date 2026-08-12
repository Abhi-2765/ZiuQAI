import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import { Calendar, Clock, Award, Eye, Share2, Edit, Trash2 } from "lucide-react";
import { quizApi } from "../api/quizApi";

export default function Host() {
    const navigate = useNavigate();
    const [quizzes, setQuizzes] = useState([]);
    const [loading, setLoading] = useState(true);

    const fetchQuizzes = async () => {
        try {
            const res = await quizApi.getMyQuizzes();
            setQuizzes(res.data);
        } catch (err) {
            console.error(err);
            toast.error("Failed to load quizzes");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchQuizzes();
    }, []);

    const copyToClipboard = async (text) => {
        try {
            if (navigator.clipboard && navigator.clipboard.writeText) {
                await navigator.clipboard.writeText(text);
                toast.success("Registration URL copied to clipboard!");
            } else {
                toast.info(`Registration URL: ${text}`);
            }
        } catch (e) {
            console.error("Clipboard copy failed", e);
            toast.error("Failed to copy link to clipboard");
        }
    };

    const handleToggleLeaderboard = async (quizId, currentVal) => {
        const newVal = !currentVal;
        setQuizzes((prev) =>
            prev.map((q) => ((q.id ?? q.quiz_id) === quizId ? { ...q, show_leaderboard: newVal } : q))
        );
        try {
            await quizApi.updateQuiz({ quiz_id: quizId, show_leaderboard: newVal });
            toast.success(`Leaderboard visibility for participants updated`);
        } catch (err) {
            console.error(err);
            toast.error("Failed to update leaderboard visibility");
            fetchQuizzes();
        }
    };

    const handleDelete = async (quizId) => {
        if (!window.confirm("Are you sure you want to delete this quiz?")) return;
        setQuizzes((prev) => prev.filter((q) => (q.id ?? q.quiz_id) !== quizId));
        try {
            await quizApi.deleteQuiz(quizId);
            toast.success("Quiz deleted successfully");
        } catch (err) {
            console.error(err);
            toast.error("Failed to delete quiz");
            fetchQuizzes();
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-slate-50 dark:bg-slate-900 flex items-center justify-center">
                <div className="w-10 h-10 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin"></div>
            </div>
        );
    }

    return (
        <div className="
            min-h-screen pt-30 pb-12 px-6 
            bg-slate-50 dark:bg-slate-900 
            text-slate-800 dark:text-slate-200
            font-roboto
        ">
            <div className="max-w-6xl mx-auto">
                <header className="mb-10 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                    <div>
                        <h1 className="text-4xl font-extrabold font-vend text-black dark:text-white">
                            Host Dashboard
                        </h1>
                        <p className="text-slate-600 dark:text-slate-400 mt-2">
                            Manage your quizzes, track registrations, and view live results.
                        </p>
                    </div>
                    <button
                        onClick={() => navigate("/generate")}
                        className="
                            px-6 py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl
                            shadow-md transition whitespace-nowrap
                        "
                    >
                        Create New Quiz
                    </button>
                </header>

                {quizzes.length === 0 ? (
                    <div className="bg-white dark:bg-slate-800 rounded-3xl p-12 text-center border border-slate-200 dark:border-slate-700 shadow-sm">
                        <Award className="w-16 h-16 mx-auto text-slate-400 mb-4" />
                        <h3 className="text-xl font-bold mb-2">No quizzes created yet</h3>
                        <p className="text-slate-500 mb-8 max-w-sm mx-auto">
                            Generate your first quiz with AI to start hosting interactive sessions.
                        </p>
                        <button
                            onClick={() => navigate("/generate")}
                            className="px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl transition"
                        >
                            Get Started
                        </button>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {quizzes.map((quiz) => {
                            const qId = quiz.id ?? quiz.quiz_id;
                            const isDraft = quiz.status === "draft";
                            const registrationUrl = `${window.location.origin}/attempt?quiz_id=${qId}`;
                            
                            let formattedDate = "N/A";
                            if (quiz.quiz_start_time) {
                                const rawStr = String(quiz.quiz_start_time);
                                const normalizedStr = (rawStr.includes("T") && !rawStr.endsWith("Z") && !rawStr.includes("+"))
                                    ? `${rawStr}Z`
                                    : rawStr;
                                const parsedDate = new Date(normalizedStr);
                                if (!isNaN(parsedDate.getTime())) {
                                    formattedDate = `${parsedDate.toLocaleDateString()} ${parsedDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
                                }
                            }
                            
                            return (
                                <div
                                    key={qId}
                                    className="
                                        bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700
                                        rounded-3xl p-6 flex flex-col justify-between hover:scale-[1.01] transition-all duration-300 shadow-sm
                                    "
                                >
                                    <div>
                                        <div className="flex justify-between items-start gap-4 mb-4">
                                            <h3 className="text-xl font-bold font-vend text-slate-900 dark:text-white line-clamp-1">
                                                {quiz.quiz_name}
                                            </h3>
                                            <span className={`
                                                px-2.5 py-1 rounded-full text-xs font-bold uppercase tracking-wider
                                                ${isDraft 
                                                    ? "bg-amber-50 dark:bg-amber-950/20 text-amber-600 dark:text-amber-400" 
                                                    : "bg-green-50 dark:bg-green-950/20 text-green-600 dark:text-green-400"}
                                            `}>
                                                {quiz.status}
                                            </span>
                                        </div>

                                        <div className="space-y-2 mb-6">
                                            <div className="flex items-center gap-2 text-sm text-slate-500 dark:text-slate-400">
                                                <Calendar size={16} />
                                                <span>{formattedDate}</span>
                                            </div>
                                            <div className="flex items-center gap-2 text-sm text-slate-500 dark:text-slate-400">
                                                <Clock size={16} />
                                                <span>{quiz.quiz_duration} mins — {quiz.question_count} Questions</span>
                                            </div>
                                            <div className="flex items-center gap-2 text-sm text-slate-500 dark:text-slate-400">
                                                <Award size={16} />
                                                <span className="capitalize">{String(quiz.quiz_difficulty || "").toLowerCase()} difficulty</span>
                                            </div>
                                        </div>
                                    </div>

                                    <div className="space-y-3">
                                        {!isDraft ? (
                                            <>
                                                <div className="flex gap-2">
                                                    <input
                                                        type="text"
                                                        readOnly
                                                        value={qId}
                                                        className="
                                                            flex-1 p-2 text-center text-sm font-mono font-bold rounded-lg
                                                            bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700
                                                            text-slate-600 dark:text-slate-300
                                                        "
                                                    />
                                                    <button
                                                        onClick={() => copyToClipboard(registrationUrl)}
                                                        className="
                                                            p-2 bg-slate-100 dark:bg-slate-700 hover:bg-slate-200 rounded-lg text-slate-600 dark:text-slate-300
                                                        "
                                                        title="Copy share link"
                                                    >
                                                        <Share2 size={18} />
                                                    </button>
                                                </div>
                                                <button
                                                    onClick={() => handleToggleLeaderboard(qId, quiz.show_leaderboard)}
                                                    className="
                                                        w-full py-2 px-3 text-xs font-bold rounded-xl border flex items-center justify-between transition
                                                        bg-slate-50 dark:bg-slate-900 border-slate-200 dark:border-slate-700 hover:border-violet-500
                                                    "
                                                >
                                                    <span className="text-slate-600 dark:text-slate-400">Participant Leaderboard:</span>
                                                    <span className={quiz.show_leaderboard ? "text-green-600 font-bold" : "text-amber-500 font-bold"}>
                                                        {quiz.show_leaderboard ? "Visible" : "Host Only"}
                                                    </span>
                                                </button>

                                                <button
                                                    onClick={() => navigate(`/standings/${qId}`)}
                                                    className="
                                                        w-full py-2.5 bg-indigo-50 dark:bg-indigo-950/20 text-indigo-600 dark:text-indigo-400 font-bold rounded-xl
                                                        hover:bg-indigo-100/50 transition border border-indigo-200 dark:border-indigo-500/30 flex items-center justify-center gap-2
                                                    "
                                                >
                                                    <Eye size={16} />
                                                    View Leaderboard
                                                </button>
                                            </>
                                        ) : (
                                            <div className="flex gap-2">
                                                <button
                                                    onClick={() => navigate(`/generate?draft=${qId}`)}
                                                    className="
                                                        flex-1 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl
                                                        transition flex items-center justify-center gap-2
                                                    "
                                                >
                                                    <Edit size={16} />
                                                    Edit Draft
                                                </button>
                                                <button
                                                    onClick={() => handleDelete(qId)}
                                                    className="
                                                        p-2.5 bg-red-50 dark:bg-red-950/20 text-red-600 dark:text-red-400 border border-red-200 dark:border-red-500/30 hover:bg-red-100 rounded-xl
                                                    "
                                                >
                                                    <Trash2 size={16} />
                                                </button>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                )}
            </div>
        </div>
    );
}
