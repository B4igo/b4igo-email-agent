import { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Box, Button, Card, TextField, Typography, Alert } from '@mui/material';
import { useSignIn } from 'react-auth-kit';
import { auth } from '../API/Auth.ts';

export default function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const signIn = useSignIn();
    const navigate = useNavigate();

    const handleSubmit: NonNullable<React.ComponentProps<'form'>['onSubmit']> = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            await auth.login(username, password, signIn);
            navigate('/');
        } catch (err: unknown) {
            if (axios.isAxiosError<{ message?: string }>(err)) {
                setError(err.response?.data?.message ?? 'Login failed');
            } else if (err instanceof Error) {
                setError(err.message || 'Login failed');
            } else {
                setError('Login failed');
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
            <Card sx={{ p: 2, maxWidth: 400, width: '100%', boxShadow: 3 }}>
                <Typography variant="h5" sx={{ mb: 2 }}>Log in to B4iGo Agentic Email Parser:</Typography>
                {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
                <Box component="form" onSubmit={handleSubmit} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                    <TextField
                        label="Username"
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                    <TextField
                        label="Password"
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                    <Button type="submit" variant="contained" disabled={loading}>
                        {loading ? 'Loading...' : 'Login'}
                    </Button>
                </Box>
            </Card>
        </Box>
    );
}
