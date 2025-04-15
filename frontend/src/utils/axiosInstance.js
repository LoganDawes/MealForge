import axios from "axios";

const axios_api = axios.create({
  baseURL: "/api",
});

let accessToken = localStorage.getItem("accessToken");
let refreshToken = localStorage.getItem("refreshToken");

const setAccessToken = (token) => {
  accessToken = token;
  localStorage.setItem("accessToken", token);
};

// Request Interceptor: Attach token unless `noAuth` is true
axios_api.interceptors.request.use((config) => {
  if (!config.noAuth && accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`;
  }
  return config;
});

// Response Interceptor: Try refresh on 401
axios_api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const originalRequest = error.config;

    if (
      error.response?.status === 500 &&
      error.response?.data?.message?.includes("401 Client Error") &&
      !originalRequest._retry &&
      !originalRequest.noAuth
    ) {
      originalRequest._retry = true;
      try {
        const res = await axios.post("/api/refresh_token/", {
          refresh_token: refreshToken,
        });

        const newAccess = res.data.access_token;
        setAccessToken(newAccess);
        originalRequest.headers.Authorization = `Bearer ${newAccess}`;

        return axios_api(originalRequest); // Retry original request
      } catch (refreshError) {
        console.error("Refresh token failed:", refreshError);
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default axios_api;
