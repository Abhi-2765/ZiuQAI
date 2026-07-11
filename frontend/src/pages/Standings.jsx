import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Trophy, Medal, Lock, ArrowLeft } from "lucide-react";
import api from "../utils/api";

export default function Standings() {
    const { quizId } = useParams();
    const navigate = useNavigate();
    const [standings, setStandings] = useState([]);
    const [loading, setLoading] = useState(true);
    const [locked, setLocked] = useState(false);
    const [lockMessage, setLockMessage] = useState("");

    const fetchLeaderboard = async () => {
        setLoading(true);
        setLocked(false);
        try {
            const res = await api.get(`/quizes/${quizId}/leaderboard`);
            setStandings(res.data);
        } catch (err) {
            console.error(err);
            if (err.response && err.response.status === 403) {
                setLocked(true);
                setLockMessage(err.response.data.detail || "Leaderboard is locked until the quiz has ended.");
            }
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchLeaderboard();
    }, [quizId]);

    if (loading) {
        return (
            <div className="min-h-screen bg-slate-50 dark:bg-slate-900 flex items-center justify-center">
                <div className="w-10 h-10 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin"></div>
            </div>
        );
    }

    return (
        <div className="
            pt-30 min-h-screen px-6 pb-12
            bg-slate-50 dark:bg-slate-900 
            text-slate-800 dark:text-slate-100
            transition-colors duration-300
        ">
            <div className="max-w-4xl mx-auto">
                <button
                    onClick={() => navigate("/dashboard")}
                    className="
                        mb-6 flex items-center gap-2 text-slate-500 hover:text-indigo-600 font-bold transition
                    "
                >
                    <ArrowLeft size={16} />
                    Back to Dashboard
                </button>

                <div className="text-center mb-12">
                    <h1 className="text-4xl font-bold flex justify-center items-center gap-3 font-vend">
                        Standings
                    </h1>
                    <p className="mt-3 text-slate-600 dark:text-slate-400">
                        See who's topping the charts in this quiz.
                    </p>
                </div>

                {locked ? (
                    <div className="
                        bg-white dark:bg-slate-800 rounded-3xl p-12 text-center border border-slate-200 dark:border-slate-700 shadow-sm
                        flex flex-col items-center justify-center gap-4 max-w-lg mx-auto
                    ">
                        <div className="w-16 h-16 bg-amber-50 dark:bg-amber-950/20 text-amber-500 rounded-2xl flex items-center justify-center">
                            <Lock size={32} />
                        </div>
                        <h3 className="text-xl font-bold">Leaderboard Locked</h3>
                        <p className="text-slate-500 dark:text-slate-400 max-w-sm mb-4">
                            {lockMessage}
                        </p>
                        <button
                            onClick={fetchLeaderboard}
                            className="px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl transition"
                        >
                            Refresh Standings
                        </button>
                    </div>
                ) : standings.length === 0 ? (
                    <div className="bg-white dark:bg-slate-800 rounded-3xl p-12 text-center border border-slate-200 dark:border-slate-700 shadow-sm">
                        <p className="text-slate-500 dark:text-slate-400">No responses submitted yet.</p>
                    </div>
                ) : (
                    <div className="space-y-4">
                        {standings.map((student) => (
                            <StandingItem
                                key={student.position}
                                {...student}
                            />
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}

const StandingItem = ({ position, name, marksObtained, totalMarks }) => {
    let rankIcon = <span className="text-xl font-bold w-8 text-center">{position}</span>;
    let rankStyles = "bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700";

    if (position === 1) {
        rankIcon = <Trophy className="w-8 h-8 text-yellow-500 fill-yellow-500/20" />;
        rankStyles = "bg-yellow-50 dark:bg-yellow-900/20 border-yellow-200 dark:border-yellow-700/50";
    } else if (position === 2) {
        rankIcon = <Medal className="w-8 h-8 text-slate-400 fill-slate-400/20" />;
        rankStyles = "bg-slate-100 dark:bg-slate-800 border-slate-300 dark:border-slate-600";
    } else if (position === 3) {
        rankIcon = <Medal className="w-8 h-8 text-amber-600 fill-amber-600/20" />;
        rankStyles = "bg-amber-50 dark:bg-amber-900/20 border-amber-200 dark:border-amber-700/50";
    }

    return (
        <div className={`
            flex items-center justify-between gap-4 p-4 md:p-6
            rounded-2xl border shadow-sm
            transition-all hover:scale-[1.01]
            ${rankStyles}
        `}>
            <div className="flex items-center gap-4">
                <div className="flex-shrink-0 w-12 flex justify-center">
                    {rankIcon}
                </div>

                <div className="flex items-center gap-3">
                    <div className="
                        w-10 h-10 rounded-full 
                        bg-linear-to-tr from-violet-500 to-fuchsia-500
                        flex items-center justify-center
                        text-white font-bold text-lg
                    ">
                        {name ? name.charAt(0).toUpperCase() : "?"}
                    </div>
                    <div>
                        <h3 className="text-lg font-bold">{name}</h3>
                    </div>
                </div>
            </div>

            <div className="flex items-center gap-6 text-right">
                <div className="text-xl font-bold">
                    {marksObtained}
                    <span className="text-slate-400 text-sm font-normal">/{totalMarks}</span>
                </div>
            </div>
        </div>
    );
};