import axios from "axios";

const ACCESS_KEY = "teqfarm_access";
const REFRESH_KEY = "teqfarm_refresh";
export const api = axios.create({ baseURL: import.meta.env.VITE_API_URL || "/api/v1", timeout: 20000 });

let refreshing;
api.interceptors.request.use((config) => {
  const token = localStorage.getItem(ACCESS_KEY);
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use((response) => response, async (error) => {
  const original = error.config;
  if (error.response?.status !== 401 || original?._retry || original?.url?.includes("auth/refresh")) {
    return Promise.reject(error);
  }
  original._retry = true;
  const refresh = localStorage.getItem(REFRESH_KEY);
  if (!refresh) return Promise.reject(error);
  try {
    refreshing ||= axios.post(`${api.defaults.baseURL}/auth/refresh/`, { refresh })
      .then(({ data }) => {
        localStorage.setItem(ACCESS_KEY, data.access);
        if (data.refresh) localStorage.setItem(REFRESH_KEY, data.refresh);
        return data.access;
      }).finally(() => { refreshing = null; });
    original.headers.Authorization = `Bearer ${await refreshing}`;
    return api(original);
  } catch (refreshError) {
    clearSession();
    return Promise.reject(refreshError);
  }
});

export function saveSession(data) {
  localStorage.setItem(ACCESS_KEY, data.access);
  localStorage.setItem(REFRESH_KEY, data.refresh);
  localStorage.setItem("teqfarm_user", JSON.stringify(data.user));
}

export function clearSession() {
  localStorage.removeItem(ACCESS_KEY);
  localStorage.removeItem(REFRESH_KEY);
  localStorage.removeItem("teqfarm_user");
  window.dispatchEvent(new Event("teqfarm:logout"));
}

export function apiError(error) {
  const data = error.response?.data;
  if (data?.errors && typeof data.errors === "object") {
    return Object.values(data.errors).flat().join(" ");
  }
  return data?.message || data?.detail || error.message || "Something went wrong.";
}

export function results(data) { return Array.isArray(data) ? data : data?.results || []; }

