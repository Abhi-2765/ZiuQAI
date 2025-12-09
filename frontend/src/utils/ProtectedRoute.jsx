import { Outlet, Navigate } from "react-router";

const ProtectedRoute = () => {
    const isAuthenticated = true;
    if (isAuthenticated) {
        return <Outlet />
    }
    else {
        return <Navigate to="/auth" />
    }
}

export default ProtectedRoute;