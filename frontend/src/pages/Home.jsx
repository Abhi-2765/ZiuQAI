import {
    FilePlusCorner,
    Sparkles,
    Crown,
    TrendingUp,
    BookmarkCheck,
    ClockArrowUp,
    UsersRound,
    ClipboardPen
} from "lucide-react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";

export default function Home() {

    const navigate = useNavigate();

    return (
        <div className="
            w-full min-h-screen pt-10
            bg-slate-50 dark:bg-slate-900 
            text-slate-800 dark:text-slate-100 
            font-vend
        ">
            <section className="max-w-6xl mx-auto text-center px-6 pt-24 pb-16">
                <h1 className="text-4xl md:text-6xl font-bold leading-tight">
                    Turn Your Study Materials <br />
                    Into Instant AI-Generated MCQs
                </h1>

                <p className="
                    mt-4 text-lg md:text-xl 
                    text-slate-600 dark:text-slate-300 
                    max-w-2xl mx-auto
                ">
                    Effortlessly create, host, and analyze quizzes using AI.
                    Get deep insights into performance and revision needs.
                </p>

                <div className="flex justify-center gap-4 mt-8">
                    <button className="
                        bg-violet-600 hover:bg-violet-700 
                        px-6 py-3 rounded-xl 
                        text-white font-semibold
                        shadow-sm
                    "
                        onClick={() => navigate("/auth")}
                    >
                        Start for Free
                    </button>

                    <button className="
                        bg-white dark:bg-slate-800 
                        border border-slate-300 dark:border-slate-700 
                        px-6 py-3 rounded-xl 
                        text-slate-700 dark:text-slate-200
                        font-semibold shadow-sm
                    "
                        onClick={() => toast.info("Demo Quiz Coming Soon!")}
                    >
                        Try Demo Quiz
                    </button>
                </div>
            </section>

            <section className="max-w-6xl mx-auto px-6 mt-20">
                <h2 className="text-center text-3xl font-bold">
                    How It Works
                </h2>
                <p className="text-center text-slate-500 dark:text-slate-400 mt-2">
                    Get started in just three simple steps.
                </p>

                <div className="
                    grid grid-cols-1 md:grid-cols-3 
                    gap-6 mt-10
                ">
                    <TutorialStep
                        icon={<FilePlusCorner className="w-10 h-10 text-violet-600 dark:text-violet-400" />}
                        text="Upload Materials"
                        desc="Securely upload PDFs, text files, or paste links to web content."
                    />
                    <TutorialStep
                        icon={<Sparkles className="w-10 h-10 text-violet-600 dark:text-violet-400" />}
                        text="AI Generates MCQs"
                        desc="AI analyzes your content and creates accurate questions instantly."
                    />
                    <TutorialStep
                        icon={<ClipboardPen className="w-10 h-10 text-violet-600 dark:text-violet-400" />}
                        text="Host or Attempt"
                        desc="Host live sessions, share quizzes, or attempt them yourself."
                    />
                </div>
            </section>

            {/* FEATURES */}
            <section className="max-w-6xl mx-auto px-6 mt-24 pb-20">
                <h2 className="text-center text-3xl font-bold">
                    Discover a Smarter Way to Learn
                </h2>
                <p className="
                    text-center text-slate-500 dark:text-slate-400 
                    mt-2 max-w-2xl mx-auto
                ">
                    ZiuQ.AI gives you powerful tools to streamline learning and assessment.
                </p>

                <div className="
                    grid grid-cols-1 md:grid-cols-2 
                    gap-6 mt-10
                ">
                    <FeatureChip
                        icon={<Sparkles />}
                        text="AI MCQ Generator"
                        desc="Automatically generate high-quality MCQs from your study materials."
                    />
                    <FeatureChip
                        icon={<TrendingUp />}
                        text="Adaptive Difficulty"
                        desc="Difficulty adjusts dynamically based on your performance."
                    />
                    <FeatureChip
                        icon={<UsersRound />}
                        text="Host Live Quizzes"
                        desc="Run interactive quiz sessions for groups or classrooms."
                    />
                    <FeatureChip
                        icon={<Crown />}
                        text="Smart Analytics"
                        desc="Understand strengths, weaknesses, and performance trends."
                    />
                    <FeatureChip
                        icon={<BookmarkCheck />}
                        text="Revision Recommendations"
                        desc="AI tells you exactly what you need to revise next."
                    />
                    <FeatureChip
                        icon={<ClockArrowUp />}
                        text="Quiz History & Tracking"
                        desc="Track past attempts, progress, and learning journeys."
                    />
                </div>
            </section>

            {/* CTA SECTION */}
            <section className="text-center py-20 bg-slate-100 dark:bg-slate-800/40">
                <h2 className="text-3xl font-bold">
                    Ready to Get Started?
                </h2>

                <div className="flex justify-center gap-4 mt-8">
                    <button className="
                        bg-violet-600 hover:bg-violet-700 
                        px-6 py-3 rounded-xl 
                        text-white font-semibold
                        shadow
                    "
                        onClick={() => navigate("/auth")}
                    >
                        Start for Free
                    </button>
                </div>
            </section>
        </div>
    );
}

const TutorialStep = ({ icon, text, desc }) => {
    return (
        <div className="
            flex flex-col items-center text-center 
            bg-white dark:bg-slate-800 
            p-8 rounded-2xl 
            shadow-sm border border-slate-200 dark:border-slate-700
        ">
            <div className="p-3 rounded-full bg-violet-100 dark:bg-violet-900/40">
                {icon}
            </div>

            <p className="text-xl font-semibold mt-4">{text}</p>

            <p className="text-sm text-slate-600 dark:text-slate-400 mt-2">
                {desc}
            </p>
        </div>
    );
};

const FeatureChip = ({ icon, text, desc }) => {
    return (
        <div className="
            flex items-start gap-4 p-5 
            bg-white dark:bg-slate-800 
            rounded-2xl shadow-sm 
            border border-slate-200 dark:border-slate-700
        ">
            <div className="text-violet-600 dark:text-violet-400">
                {icon}
            </div>

            <div>
                <p className="text-lg font-semibold">{text}</p>
                <p className="text-sm text-slate-600 dark:text-slate-400">{desc}</p>
            </div>
        </div>
    );
};