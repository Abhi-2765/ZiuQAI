import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthProvider";
import { authApi } from "../api/authApi";
import { toast } from "react-toastify";

function Profile() {
    const { setEmail, setName } = useAuth();
    const navigate = useNavigate();

    const handleLogout = async () => {
        try {
            setEmail(null);
            setName(null);
            const response = await authApi.logout();
            toast.success(response.data.message || "Logout successful");
            navigate("/auth", { state: { isLogin: true } });
        } catch (error) {
            toast.error(error?.response?.data?.detail || "Failed to logout");
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center pt-24">
            <button
                onClick={handleLogout}
                className="px-6 py-3 bg-red-600 hover:bg-red-700 text-white font-bold rounded-xl shadow-md transition-all"
            >
                Logout
            </button>
        </div>
    );
}

export default Profile;