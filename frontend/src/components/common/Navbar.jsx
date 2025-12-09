import Logo from "./Logo";
import ThemeChanger from "./ThemeChanger";
import NavLink from "./NavLink";

const Navbar = () => {
    return (
        <div>
            <Logo />
            <ThemeChanger />
            <NavLink text="Home" route="home" />
            <NavLink text="About" route="about" />
            <NavLink text="Contact" route="contact" />
        </div>
    )
}

export default Navbar;