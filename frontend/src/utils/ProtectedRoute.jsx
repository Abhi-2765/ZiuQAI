import { Outlet, Navigate } from "react-router";
import { useAuth } from "../context/AuthProvider";

const ProtectedRoute = () => {
    const { loading, email } = useAuth();

    if (loading) {
        return <div>Loading...</div>;
    }

    if (email) {
        return <Outlet />; // render nested routes
    } else {
        return <Navigate to="/auth" />; // redirect to login
    }
};

export default ProtectedRoute;