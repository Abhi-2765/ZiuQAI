import { createContext, useContext, useState } from "react";

const AuthContext = createContext();

const AuthProvider = ({ children }) => {
    const [email, setEmail] = useState(null);
    const [name, setName] = useState(null);
    const [loading, setLoading] = useState(false);

    return (
        <AuthContext.Provider value={{ email, setEmail, name, setName, loading, setLoading }}>
            {children}
        </AuthContext.Provider>
    );
};