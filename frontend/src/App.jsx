import { Route, Routes } from "react-router"
import ProtectedRoute from "./utils/ProtectedRoute"
import Navbar from "./components/Navbar/Navbar"
import Footer from "./components/Footer/Footer"
import Authenticate from "./pages/Authenticate"
import { useLocation } from "react-router"
import Dashboard from "./pages/Dashboard"
import GenerateQuiz from "./pages/GenerateQuiz"
import Loading from "./components/common/Loading"
import Home from "./pages/Home"

const App = () => {
  const location = useLocation()
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/auth" element={<Authenticate />} />
        <Route path="/" element={<Home />} />

        <Route element={<ProtectedRoute />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/generate" element={<GenerateQuiz />} />
          <Route path="/host" element={<></>} />
          <Route path="/attempt" element={<></>} />
          <Route path="/profile" element={<></>} />
        </Route>
      </Routes>
      {location.pathname === "/" && <Footer />}
    </>
  )
}

export default App