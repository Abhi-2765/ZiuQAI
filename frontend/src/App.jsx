import { Route, Routes } from "react-router"
import ThemeChanger from "./components/common/ThemeChanger"
import ProtectedRoute from "./utils/ProtectedRoute"
import Navbar from "./components/Navbar/Navbar"
import Footer from "./components/Footer/Footer"
import Authenticate from "./pages/Authenticate"
import { useLocation } from "react-router"

const App = () => {
  const location = useLocation()
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/auth" element={<Authenticate />} />
        <Route path="/" element={<p>Hi</p>} />

        <Route element={<ProtectedRoute />}>
          <Route path="/dashboard" element={<div>Dashboard</div>} />
        </Route>
      </Routes>
      {location.pathname === "/" && <Footer />}
    </>
  )
}

export default App