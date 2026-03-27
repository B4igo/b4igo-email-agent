import { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    Box,
    Container,
    Typography,
    CircularProgress,
    Button,
    Stack
} from '@mui/material';
import {EmailConnectorFlow} from "../Functions/EmailConnectorFlow.ts";

export function ProviderCallbackPage() {
    const navigate = useNavigate();
    const [error, setError] = useState<string>('');
    const callbackInProgress = useRef(false);

    useEffect(() => {
        if (callbackInProgress.current) return;
        callbackInProgress.current = true;
        handleCallback();
    }, []);

    const handleCallback = async () => {
        const result = await EmailConnectorFlow.handleProviderCallback();

        if (result.success) {
            navigate('/email-connectors');
        } else {
            setError(result.error || 'Unknown error occurred');
        }
    };

    return (
        <Container maxWidth="sm">
            <Box sx={{ mt: 8, mb: 4 }}>
                <Stack spacing={3} alignItems="center">
                    {!error ? (
                        <>
                            <CircularProgress size={60} />
                            <Typography variant="h5" component="h2" align="center">
                                Finishing connector setup...
                            </Typography>
                        </>
                    ) : (
                        <>
                            <Typography variant="h5" component="h2" color="error" align="center">
                                Error: {error}
                            </Typography>
                            <Button
                                variant="contained"
                                onClick={() => navigate('/email-connectors')}
                            >
                                Back
                            </Button>
                        </>
                    )}
                </Stack>
            </Box>
        </Container>
    );
}