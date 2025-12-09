import { Link, useLocation } from "react-router";

const NavLink = ({ text, route }) => {
    const { pathname } = useLocation();
    const isActive = pathname === `/${route}`;

    return (
        <Link
            to={`/${route}`}
            className={`
                px-4 py-2 text-sm font-medium rounded-full transition-all duration-300
                select-none
                ${isActive
                    ? "bg-slate-900 text-white dark:bg-white dark:text-slate-900"
                    : "text-slate-700 dark:text-slate-300 hover:bg-black-200/70 dark:hover:bg-slate-700/50"
                }
            `}
        >
            {text}
        </Link>
    );
};

export default NavLink;
