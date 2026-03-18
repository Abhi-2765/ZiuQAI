import { useState } from "react";
import GeneralChip from "../components/Dashboard/GeneralChip";
import RouteChip from "../components/Dashboard/RouteChip";
import ActivityChip from "../components/Dashboard/ActivityChip";

const Dashboard = () => {
    const [name] = useState("Alex");

    const generalHistory = [
        { label: "Quizzes Attempted", count: 12 },
        { label: "Hosted", count: 3 }
    ];

    const features = [
        {
            key: "generate",
            label: "Generate Quiz with AI",
            description: "Create engaging quizzes in minutes using AI.",
            icon: "✨",
            route: "/generate"
        },
        {
            key: "host",
            label: "Host a Live Quiz",
            description: "Start a real-time quiz session for your audience.",
            icon: "📡",
            route: "/host"
        },
        {
            key: "attempt",
            label: "Attempt a Quiz",
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
