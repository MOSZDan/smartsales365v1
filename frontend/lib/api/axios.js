import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

// Create axios instance
const axiosInstance = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor to add auth token
axiosInstance.interceptors.request.use(
    (config) => {
        if (typeof window !== 'undefined') {
            const token = localStorage.getItem('access_token');
            if (token) {
                config.headers.Authorization = `Bearer ${token}`;
            }
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor to handle token refresh
axiosInstance.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        // If error is 401 and we haven't tried to refresh token yet
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            if (typeof window !== 'undefined') {
                const refreshToken = localStorage.getItem('refresh_token');

                if (refreshToken) {
                    try {
                        const response = await axios.post(`${API_URL}/auth/token/refresh/`, {
                            refresh: refreshToken,
                        });

                        const { access } = response.data;
                        localStorage.setItem('access_token', access);

                        // Retry original request with new token
                        originalRequest.headers.Authorization = `Bearer ${access}`;
                        return axiosInstance(originalRequest);
                    } catch (refreshError) {
                        // Refresh token is invalid, logout user
                        localStorage.removeItem('access_token');
                        localStorage.removeItem('refresh_token');
                        localStorage.removeItem('user');
                        window.location.href = '/login';
                        return Promise.reject(refreshError);
                    }
                } else {
                    // No refresh token available
                    window.location.href = '/login';
                }
            }
        }

        return Promise.reject(error);
    }
);

export default axiosInstance;
