import { Link, useLocation } from "react-router";

const NavLink = ({ text, route, isAuth = false }) => {
    const { pathname } = useLocation();
    const fullRoute = route.startsWith("/") ? route : `/${route}`;
    const isActive = pathname === fullRoute;

    return (
        <Link
            to={fullRoute}
            className={`
                px-4 py-2 
                text-sm font-medium 
                rounded-full 
                transition-all duration-300 
                select-none
                ${isActive
                    ? "bg-slate-900 text-white dark:bg-white dark:text-slate-900 shadow-sm"
                    : "text-slate-700 dark:text-slate-300 hover:bg-slate-300/40 dark:hover:bg-slate-700/50"
                }
                ${isAuth ? "bg-black text-white dark:text-slate-900 dark:bg-white shadow-sm" : ""}
            `}
        >
            {text}
        </Link>
    );
};

export default NavLink;
