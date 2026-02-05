import axios from 'axios';

const BACKEND_URL = 'http://localhost:5000/api';

const api = axios.create({
    baseURL: BACKEND_URL,
});

api.interceptors.request.use((config) => {
    const token = localStorage.getItem('_auth');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                const refreshToken = localStorage.getItem('_auth_refresh');
                const { data } = await axios.post(`${BACKEND_URL}/auth/refresh`, {
                    refresh_token: refreshToken
                });

                localStorage.setItem('_auth', data.access_token);
                originalRequest.headers.Authorization = `Bearer ${data.access_token}`;

                return api(originalRequest);
            } catch (refreshError) {
                localStorage.clear();
                window.location.href = '/login';
                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);


export const auth = {
    async login(email: string, password: string, signIn: any) {
        const { data } = await axios.post(`${BACKEND_URL}/auth/login`, {
            username: email,
            password
        });

        if (data.refresh_token) {
            localStorage.setItem('_auth_refresh', data.refresh_token);
        }

        const success = signIn({
            token: data.access_token,
            expiresIn: 3600,
            tokenType: 'Bearer',
            authState: { email }
        });

        if (!success) {
            throw new Error('Authentication failed');
        }

        return data;
    },

    async logout() {
        try {
            await api.post('/auth/logout');
        } finally {
            localStorage.clear();
        }
    },
};

export { api };
