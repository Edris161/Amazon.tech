import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/api/",
});

// Attach access token to every request
api.interceptors.request.use(
  (config) => {
    if (typeof window !== "undefined") {
      const token = localStorage.getItem("access");
      if (token && config.headers) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Handle token expiration + auto refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If access token expired (401) and we haven't retried yet
    if (
      error.response?.status === 401 &&
      !originalRequest._retry &&
      typeof window !== "undefined"
    ) {
      originalRequest._retry = true;

      const refreshToken = localStorage.getItem("refresh");

      if (!refreshToken) {
        localStorage.removeItem("access");
        window.location.href = "/login";
        return Promise.reject(error);
      }

      try {
        const response = await axios.post(
          "http://localhost:8000/api/auth/refresh/",
          { refresh: refreshToken }
        );

        const newAccess = response.data.access;

        localStorage.setItem("access", newAccess);

        // Retry original request with new token
        originalRequest.headers.Authorization = `Bearer ${newAccess}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Refresh failed → force logout
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
        window.location.href = "/login";
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;