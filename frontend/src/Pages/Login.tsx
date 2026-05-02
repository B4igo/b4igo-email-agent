import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Card, Typography, Alert, CircularProgress } from '@mui/material';
import { useSignIn } from 'react-auth-kit';
import { auth } from '../API/Auth.ts';

declare const chrome: any;

export default function Login() {
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const signIn = useSignIn();
    const navigate = useNavigate();

    const handleLogin = useCallback(async () => {
        if (loading) return;

        setError('');
        setLoading(true);

        try {
            await auth.performSiweFlow(signIn);
            navigate('/');
        } catch (err: any) {
            setError(err.message || 'Authentication failed');
            setLoading(false);
        }
    }, [loading, navigate, signIn]);

    useEffect(() => {
        const checkKeysAndLogin = async () => {
            if (loading || error) return;

            let keys = localStorage.getItem("allPrivateKeys");

            if (!keys && typeof chrome !== 'undefined' && chrome.storage && chrome.storage.local) {
                const result = await new Promise<{ allPrivateKeys?: string }>((resolve) => {
                    chrome.storage.local.get(['allPrivateKeys'], (res: any) => resolve(res as any));
                });
                keys = result.allPrivateKeys || null;
            }

            if (keys) {
                handleLogin();
            }
        };

        const interval = setInterval(checkKeysAndLogin, 3000);
        checkKeysAndLogin();

        return () => clearInterval(interval);
    }, [handleLogin, loading, error]);

    useEffect(() => {
        if (error) {
            const timer = setTimeout(() => setError(''), 10000);
            return () => clearTimeout(timer);
        }
    }, [error]);

    return (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh', bgcolor: '#f5f5f5' }}>
            <Card sx={{ p: 4, maxWidth: 450, width: '100%', boxShadow: 3, textAlign: 'center' }}>
                <Typography variant="h5" sx={{ mb: 3, fontWeight: 'bold', color: '#1976d2' }}>
                    B4iGo Agentic Email Parser
                </Typography>

                <Box sx={{ my: 4, minHeight: '100px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
                    {loading ? (
                        <>
                            <CircularProgress size={40} sx={{ mb: 2 }} />
                            <Typography variant="body1" color="text.secondary">
                                Authenticating with B4iGo keys...
                            </Typography>
                        </>
                    ) : (
                        <>
                            <Typography variant="body1" sx={{ fontWeight: 500 }}>
                                Waiting for Authentication Keys
                            </Typography>
                            <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                                Please ensure you are logged into the B4iGo extension.
                                This page will refresh automatically once keys are detected.
                            </Typography>
                        </>
                    )}
                </Box>

                {error && (
                    <Alert severity="error" sx={{ mt: 2, textAlign: 'left' }}>
                        {error}
                    </Alert>
                )}
            </Card>
        </Box>
    );
}