import Logo from "../common/Logo";
import ThemeChanger from "../common/ThemeChanger";
import NavLink from "./NavLink";
import { useState } from "react";
import { useLocation, useNavigate } from "react-router";

const Navbar = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const isLandingPage = location.pathname === "/" || location.pathname === "/auth";
    const [login, setLogin] = useState(false);

    const handleClick = () => {
        if (!login) {
            navigate("/");
        } else {
            navigate("/dashboard");
        }
    }


    return (
        <nav
            className="
                fixed top-4 left-1/2 -translate-x-1/2 
                w-[92%] md:w-[80%] 
                backdrop-blur-xl 
                bg-white/70 dark:bg-slate-900 
                border border-slate-300/40 dark:border-slate-700/40
                shadow-[0_4px_20px_rgba(0,0,0,0.08)]
                rounded-2xl 
                px-6 py-3 
                flex items-center justify-between 
                z-50
            "
        >
            <div className="flex items-center gap-3 cursor-pointer" onClick={() => handleClick()}>
                <Logo text="SquirrelAI" textSize="text-4xl" iconSize="w-12 h-12" />
            </div>

            <>
                {isLandingPage ? (
                    <>
                        <div className="flex-1"></div>
                        <div className="hidden md:flex justify-end items-center gap-4 mx-4">
                            <NavLink text="Get Started" route="auth" isAuth={true} />
                        </div>
                    </>
                ) : (
                    <>
                        <div className="hidden md:flex justify-center items-center gap-4">
                            <NavLink text="Dashboard" route="dashboard" />
                            <NavLink text="Generate" route="generate" />
                            <NavLink text="Host" route="host" />
                            <NavLink text="Participate" route="participate" />
                            <NavLink text="Profile" route="profile" />
                        </div>
                    </>
                )}
            </>

            <div className="flex items-center gap-3">
                <ThemeChanger />
            </div>
        </nav>
    )
};

export default Navbar;
