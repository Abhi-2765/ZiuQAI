export default function Navigation({ questions }) {
    return (
        <div className="
            w-full max-w-xs 
            bg-white dark:bg-slate-800 
            border border-slate-200 dark:border-slate-700 
            rounded-2xl p-5 shadow-sm
        ">
            <p className="text-lg font-semibold mb-4">
                Question Navigator
            </p>

            <div className="
                grid grid-cols-5 gap-3
            ">
                {questions.map((q, index) => (
                    <NavBtn
                        key={index}
                        questionIdx={index + 1}
                        status={q.status}
                    />
                ))}
            </div>

            <div className="mt-6">
                <p className="text-sm font-semibold mb-3">
                    Legend
                </p>

                <div className="flex flex-col gap-2 text-sm">
                    <LegendItem color="bg-red-600" label="Not Attempted" />
                    <LegendItem color="bg-green-600" label="Attempted" />
                    <LegendItem color="bg-violet-600" label="Marked for Review" />
                    <LegendItem color="bg-slate-300 dark:bg-slate-600" label="Not Visited" />
                </div>
            </div>
        </div>
    );
}

const NavBtn = ({ questionIdx, status }) => {
    const baseStyles = `
        w-10 h-10 flex items-center justify-center 
        rounded-full font-semibold text-sm 
        transition border shadow-sm
    `;

    const statusStyles = {
        complete: `
            bg-green-600 text-white 
            border-green-700 
            hover:bg-green-700
        `,
        markForReview: `
            bg-violet-600 text-white 
            border-violet-700 
            hover:bg-violet-700
        `,
        notVisited: `
            bg-slate-200 text-slate-700 
            dark:bg-slate-700 dark:text-slate-300
            border-slate-300 dark:border-slate-600
            hover:border-violet-600 hover:text-violet-600
        `,
        current: `
            bg-red-600 text-white 
            border-red-700 
            hover:bg-red-700
        `
    };

    return (
        <button
            className={`${baseStyles} ${statusStyles[status] || statusStyles.notVisited}`}
        >
            {questionIdx}
        </button>
    );
};

const LegendItem = ({ color, label }) => (
    <div className="flex items-center gap-2">
        <div className={`w-4 h-4 rounded-full ${color}`}></div>
        <span className="text-slate-600 dark:text-slate-300">{label}</span>
    </div>
);
