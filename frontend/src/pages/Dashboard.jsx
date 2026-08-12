import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import GeneralChip from "../components/Dashboard/GeneralChip";
import RouteChip from "../components/Dashboard/RouteChip";
import ActivityChip from "../components/Dashboard/ActivityChip";
import { useAuth } from "../context/AuthProvider";
import { FileText, Clock, ArrowRight } from "lucide-react";
import { quizApi } from "../api/quizApi";

const Dashboard = () => {
    const { name } = useAuth();
    const navigate = useNavigate();
    const [drafts, setDrafts] = useState([]);

    useEffect(() => {
        loadDrafts();
    }, []);

    const loadDrafts = async () => {
        try {
            const res = await quizApi.getMyDrafts();
            setDrafts(res.data || []);
        } catch (err) {
            console.error("Failed to load drafts:", err);
        }
    };

    const generalHistory = [
        { label: "Quizzes Attempted", count: 12 },
        { label: "Hosted", count: 3 }
    ];

    const features = [
        {
            key: "generate",
            label: "Generate quiz with AI",
            description: "Create engaging quizzes in minutes using AI.",
            icon: "✨",
            route: "/generate"
        },
        {
            key: "host",
            label: "Host a quiz",
            description: "Start a real-time quiz session for your audience.",
            icon: "📡",
            route: "/host"
        },
        {
            key: "attempt",
            label: "Attempt a quiz",
            description: "Test your knowledge with new quizzes.",
            icon: "❓",
            route: "/attempt"
        }
    ];

    const recentActivity = [
        {
            quizName: "History of Ancient Rome",
            date: "Oct 26, 2023",
            score: 9,
            percentage: 90,
            difficulty: "Hard"
        },
        {
            quizName: "General Knowledge 101",
            date: "Oct 24, 2023",
            score: 10,
            percentage: 100,
            difficulty: "Easy"
        },
        {
            quizName: "Calculus Basics",
            date: "Oct 22, 2023",
            score: 7,
            percentage: 70,
            difficulty: "Medium"
        },
        {
            quizName: "World War II Trivia",
            date: "Oct 20, 2023",
            score: 8,
            percentage: 80,
            difficulty: "Hard"
        }
    ];

    return (
        <div className="
            w-full min-h-screen 
            px-4 md:px-8 lg:px-16 pt-30 pb-10
            bg-slate-50 dark:bg-slate-900 
            text-slate-800 dark:text-slate-100 
            font-roboto
        ">
            <p className="text-3xl font-vend font-bold">
                Welcome back, {name}!
            </p>

            <div className="flex flex-wrap mt-6 gap-3">
                {generalHistory.map((item, index) => (
                    <GeneralChip key={index} {...item} />
                ))}
            </div>

            {drafts.length > 0 && (
                <>
                    <p className="text-2xl font-vend font-bold mt-12 mb-4 flex items-center gap-2">
                        <FileText size={24} className="text-amber-500" />
                        Draft Quizzes
                    </p>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {drafts.map((draft) => (
                            <div
                                key={draft.quiz_id}
                                className="
                                    bg-white dark:bg-slate-800 
                                    rounded-2xl border border-amber-200 dark:border-amber-700/40
                                    p-5 shadow-sm hover:shadow-md transition-all duration-200
                                    group cursor-pointer
                                "
                                onClick={() => navigate(`/generate?draft=${draft.quiz_id}`)}
                            >
                                <div className="flex items-start justify-between mb-3">
                                    <div className="flex-1 min-w-0">
                                        <h3 className="font-bold text-slate-800 dark:text-slate-100 truncate">
                                            {draft.quiz_name}
                                        </h3>
                                        <div className="flex items-center gap-3 mt-1.5 text-xs text-slate-500">
                                            <span>{draft.question_count} questions</span>
                                            <span>•</span>
                                            <span className={`font-semibold ${draft.quiz_difficulty === "EASY" ? "text-green-500" :
                                                draft.quiz_difficulty === "MEDIUM" ? "text-amber-500" :
                                                    "text-red-500"
                                                }`}>{draft.quiz_difficulty}</span>
                                            <span>•</span>
                                            <span>{draft.resource_count} file{draft.resource_count !== 1 ? 's' : ''}</span>
                                        </div>
                                    </div>
                                    <div className="w-8 h-8 rounded-lg bg-amber-50 dark:bg-amber-900/20 flex items-center justify-center text-amber-500 group-hover:bg-amber-100 dark:group-hover:bg-amber-900/40 transition">
                                        <ArrowRight size={16} />
                                    </div>
                                </div>
                                <div className="flex items-center gap-1.5 text-xs text-slate-400">
                                    <Clock size={12} />
                                    <span>{draft.created_at ? new Date(draft.created_at).toLocaleDateString() : "Unknown"}</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </>
            )}

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-10">
                {features.map(({ key, ...featureProps }) => (
                    <RouteChip key={key} {...featureProps} />
                ))}
            </div>

            <p className="text-3xl font-vend font-bold mt-12 mb-4">
                Your Recent Activity
            </p>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {recentActivity.map((item, idx) => (
                    <ActivityChip key={idx} {...item} />
                ))}
            </div>

        </div>
    );
};

export default Dashboard;
