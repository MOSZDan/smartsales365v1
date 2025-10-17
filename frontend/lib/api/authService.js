import axiosInstance from './axios';

const authService = {
    // Register new user
    register: async (userData) => {
        const response = await axiosInstance.post('/auth/register/', userData);
        if (response.data.tokens) {
            localStorage.setItem('access_token', response.data.tokens.access);
            localStorage.setItem('refresh_token', response.data.tokens.refresh);
            localStorage.setItem('user', JSON.stringify(response.data.user));
        }
        return response.data;
    },

    // Login user
    login: async (credentials) => {
        const response = await axiosInstance.post('/auth/login/', credentials);
        if (response.data.tokens) {
            localStorage.setItem('access_token', response.data.tokens.access);
            localStorage.setItem('refresh_token', response.data.tokens.refresh);
            localStorage.setItem('user', JSON.stringify(response.data.user));
        }
        return response.data;
    },

    // Logout user
    logout: async () => {
        const refreshToken = localStorage.getItem('refresh_token');
        try {
            await axiosInstance.post('/auth/logout/', {
                refresh_token: refreshToken
            });
        } catch (error) {
            console.error('Logout error:', error);
        } finally {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('user');
        }
    },

    // Get current user profile
    getProfile: async () => {
        const response = await axiosInstance.get('/auth/profile/');
        return response.data;
    },

    // Update user profile
    updateProfile: async (userData) => {
        const response = await axiosInstance.put('/auth/profile/', userData);
        localStorage.setItem('user', JSON.stringify(response.data));
        return response.data;
    },

    // Change password
    changePassword: async (passwordData) => {
        const response = await axiosInstance.post('/auth/change-password/', passwordData);
        return response.data;
    },

    // Request password reset
    requestPasswordReset: async (email) => {
        const response = await axiosInstance.post('/auth/password-reset/', { email });
        return response.data;
    },

    // Confirm password reset
    confirmPasswordReset: async (resetData) => {
        const response = await axiosInstance.post('/auth/password-reset-confirm/', resetData);
        return response.data;
    },

    // Get user from localStorage
    getCurrentUser: () => {
        if (typeof window !== 'undefined') {
            const user = localStorage.getItem('user');
            return user ? JSON.parse(user) : null;
        }
        return null;
    },

    // Check if user is authenticated
    isAuthenticated: () => {
        if (typeof window !== 'undefined') {
            return !!localStorage.getItem('access_token');
        }
        return false;
    }
};

export default authService;
