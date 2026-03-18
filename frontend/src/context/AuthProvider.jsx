import { createContext, useContext, useEffect, useState } from "react";
import api from "../utils/api";

export const AuthContext = createContext();

const AuthProvider = ({ children }) => {
    const [email, setEmail] = useState(null);
    const [name, setName] = useState(null);
    const [loading, setLoading] = useState(true);

    const fetchUser = async () => {
        try {
            const res = await api.get("/auth/me");
            setEmail(res.data.email);
            setName(res.data.username);
        } catch {
            setEmail(null);
            setName(null);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchUser();
    }, []);

    return (
        <AuthContext.Provider value={{ email, name, loading, setEmail, setName, fetchUser }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
export default AuthProvider;