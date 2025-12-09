import { Route, Routes } from "react-router"
import ThemeChanger from "./components/common/ThemeChanger"
import ProtectedRoute from "./utils/ProtectedRoute"
import Navbar from "./components/common/Navbar"

const App = () => {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/auth" element={<div>Login</div>} />
        <Route path="/" element={<ThemeChanger />} />

        <Route element={<ProtectedRoute />}>
          <Route path="/dashboard" element={<div>Dashboard</div>} />
        </Route>
      </Routes>
    </>
  )
}

export default App