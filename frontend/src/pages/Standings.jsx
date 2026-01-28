import { useState } from "react";
import { Trophy, Medal, Crown } from "lucide-react";

export default function Standings() {
    const [standings, setStandings] = useState([
        {
            "position": 1,
            "name": "Abhiram",
            "marksObtained": 58,
            "totalMarks": 60
        },
        {
            "position": 2,
            "name": "Sarah",
            "marksObtained": 55,
            "totalMarks": 60
        },
        {
            "position": 3,
            "name": "Mike",
            "marksObtained": 52,
            "totalMarks": 60
        },
        {
            "position": 4,
            "name": "Jessica",
            "marksObtained": 48,
            "totalMarks": 60
        },
        {
            "position": 5,
            "name": "David",
            "marksObtained": 45,
            "totalMarks": 60
        }
    ]);

    return (
        <div className="
            pt-30 min-h-screen px-6
            bg-slate-50 dark:bg-slate-900 
            text-slate-800 dark:text-slate-100
            transition-colors duration-300
        ">
            <div className="max-w-4xl mx-auto">
                <div className="text-center mb-12">
                    <h1 className="text-4xl font-bold flex justify-center items-center gap-3">
                        Standings
                    </h1>
                    <p className="mt-3 text-slate-600 dark:text-slate-400">
                        See who's topping the charts in the participants.
                    </p>
                </div>

                <div className="space-y-4">
                    {standings.map((student) => (
                        <StandingItem
                            key={student.position}
                            {...student}
                        />
                    ))}
                </div>
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
        rankIcon = <Medal className="w-8 h-8 text-slate-400 fill-slate-400/20" />; // Silver-ish
        rankStyles = "bg-slate-100 dark:bg-slate-800 border-slate-300 dark:border-slate-600";
    } else if (position === 3) {
        rankIcon = <Medal className="w-8 h-8 text-amber-600 fill-amber-600/20" />; // Bronze
        rankStyles = "bg-amber-50 dark:bg-amber-900/20 border-amber-200 dark:border-amber-700/50";
    }

    const percentage = Math.round((marksObtained / totalMarks) * 100);

    return (
        <div className={`
            flex items-center gap-4 p-4 md:p-6
            rounded-2xl border shadow-sm
            transition-all hover:scale-[1.01]
            ${rankStyles}
        `}>
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
                    {name.charAt(0)}
                </div>
                <div>
                    <h3 className="text-lg font-bold">{name}</h3>
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