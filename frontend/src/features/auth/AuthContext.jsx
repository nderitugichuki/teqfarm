import { createContext, useContext, useEffect, useMemo, useState } from "react";
import { api, clearSession, saveSession } from "../../lib/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    try { return JSON.parse(localStorage.getItem("teqfarm_user")); } catch { return null; }
  });
  const [ready, setReady] = useState(false);

  useEffect(() => {
    const signedOut = () => setUser(null);
    window.addEventListener("teqfarm:logout", signedOut);
    if (localStorage.getItem("teqfarm_access")) {
      api.get("/auth/profile/").then(({ data }) => {
        setUser(data); localStorage.setItem("teqfarm_user", JSON.stringify(data));
      }).catch(clearSession).finally(() => setReady(true));
    } else setReady(true);
    return () => window.removeEventListener("teqfarm:logout", signedOut);
  }, []);

  const value = useMemo(() => ({
    user, ready,
    async login(credentials) {
      const { data } = await api.post("/auth/login/", credentials);
      saveSession(data); setUser(data.user); return data.user;
    },
    async logout() {
      const refresh = localStorage.getItem("teqfarm_refresh");
      try { if (refresh) await api.post("/auth/logout/", { refresh }); } finally { clearSession(); }
    },
    setUser,
    canManage: user?.is_superuser || ["administrator", "manager"].includes(user?.role),
  }), [user, ready]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() { return useContext(AuthContext); }

