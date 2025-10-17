import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import authService from '@/lib/api/authService';

// Get user from localStorage
const user = typeof window !== 'undefined' ? authService.getCurrentUser() : null;

const initialState = {
    user: user,
    isAuthenticated: !!user,
    isLoading: false,
    isSuccess: false,
    isError: false,
    message: '',
};

// Register user
export const register = createAsyncThunk(
    'auth/register',
    async (userData, thunkAPI) => {
        try {
            return await authService.register(userData);
        } catch (error) {
            const message =
                (error.response && error.response.data && error.response.data.message) ||
                error.message ||
                error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

// Login user
export const login = createAsyncThunk(
    'auth/login',
    async (credentials, thunkAPI) => {
        try {
            return await authService.login(credentials);
        } catch (error) {
            const message =
                (error.response && error.response.data && error.response.data.message) ||
                error.message ||
                error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

// Logout user
export const logout = createAsyncThunk('auth/logout', async (_, thunkAPI) => {
    try {
        await authService.logout();
    } catch (error) {
        const message =
            (error.response && error.response.data && error.response.data.message) ||
            error.message ||
            error.toString();
        return thunkAPI.rejectWithValue(message);
    }
});

// Get user profile
export const getProfile = createAsyncThunk(
    'auth/getProfile',
    async (_, thunkAPI) => {
        try {
            return await authService.getProfile();
        } catch (error) {
            const message =
                (error.response && error.response.data && error.response.data.message) ||
                error.message ||
                error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

// Update user profile
export const updateProfile = createAsyncThunk(
    'auth/updateProfile',
    async (userData, thunkAPI) => {
        try {
            return await authService.updateProfile(userData);
        } catch (error) {
            const message =
                (error.response && error.response.data && error.response.data.message) ||
                error.message ||
                error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        reset: (state) => {
            state.isLoading = false;
            state.isSuccess = false;
            state.isError = false;
            state.message = '';
        },
        setUser: (state, action) => {
            state.user = action.payload;
            state.isAuthenticated = !!action.payload;
        },
    },
    extraReducers: (builder) => {
        builder
            // Register
            .addCase(register.pending, (state) => {
                state.isLoading = true;
            })
            .addCase(register.fulfilled, (state, action) => {
                state.isLoading = false;
                state.isSuccess = true;
                state.isAuthenticated = true;
                state.user = action.payload.user;
            })
            .addCase(register.rejected, (state, action) => {
                state.isLoading = false;
                state.isError = true;
                state.message = action.payload;
                state.user = null;
                state.isAuthenticated = false;
            })
            // Login
            .addCase(login.pending, (state) => {
                state.isLoading = true;
            })
            .addCase(login.fulfilled, (state, action) => {
                state.isLoading = false;
                state.isSuccess = true;
                state.isAuthenticated = true;
                state.user = action.payload.user;
            })
            .addCase(login.rejected, (state, action) => {
                state.isLoading = false;
                state.isError = true;
                state.message = action.payload;
                state.user = null;
                state.isAuthenticated = false;
            })
            // Logout
            .addCase(logout.fulfilled, (state) => {
                state.user = null;
                state.isAuthenticated = false;
                state.isLoading = false;
                state.isSuccess = false;
                state.isError = false;
                state.message = '';
            })
            // Get Profile
            .addCase(getProfile.pending, (state) => {
                state.isLoading = true;
            })
            .addCase(getProfile.fulfilled, (state, action) => {
                state.isLoading = false;
                state.user = action.payload;
            })
            .addCase(getProfile.rejected, (state, action) => {
                state.isLoading = false;
                state.isError = true;
                state.message = action.payload;
            })
            // Update Profile
            .addCase(updateProfile.pending, (state) => {
                state.isLoading = true;
            })
            .addCase(updateProfile.fulfilled, (state, action) => {
                state.isLoading = false;
                state.isSuccess = true;
                state.user = action.payload;
            })
            .addCase(updateProfile.rejected, (state, action) => {
                state.isLoading = false;
                state.isError = true;
                state.message = action.payload;
            });
    },
});

export const { reset, setUser } = authSlice.actions;
export default authSlice.reducer;
