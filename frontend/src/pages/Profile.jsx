import { useNavigate } from "react-router"
import { useAuth } from "../context/AuthProvider"
import api from "../utils/api"
import { toast } from "react-toastify"

function Profile() {
    const { email, name, setEmail, setName } = useAuth()

    const navigate = useNavigate();

    const handleLogout = async () => {
        try {
            setEmail(null)
            setName(null)
            const response = await api.post("/auth/logout")
            toast.success(response.data)

            navigate("/auth", { state: { isLogin: true } })
        } catch (error) {
            toast.error(error.response.data)
        }
    }

    return (
        <div>
            <button onClick={handleLogout}>
                Logout
            </button>
        </div>
    )
}

export default Profile