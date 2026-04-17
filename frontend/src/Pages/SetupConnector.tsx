import {useEffect, useState} from "react";
import {useParams, useNavigate, useSearchParams} from "react-router-dom";
import {
    Box,
    Button,
    Container,
    Typography,
    Paper,
    CircularProgress,
    Stack,
    TextField,
    FormControlLabel,
    Checkbox
} from '@mui/material';
import type {EmailSetupStep} from "../Domain/EmailConnector.ts";
import {emailConnectors} from "../API/EmailConnectors.ts";
import {EmailConnectorFlow} from "../Functions/EmailConnectorFlow.ts";

export function SetupConnectorPage() {
    const { providerType } = useParams<{ providerType: string }>();
    const [searchParams] = useSearchParams();
    const connectorName = searchParams.get('name') || '';
    const navigate = useNavigate();

    const [loading, setLoading] = useState(true);
    const [steps, setSteps] = useState<EmailSetupStep[]>([]);
    const [currentStepIndex, setCurrentStepIndex] = useState(0);
    const [submitting, setSubmitting] = useState(false);
    const [errorMsg, setErrorMsg] = useState('');
    const [polling, setPolling] = useState(false);

    useEffect(() => {
        loadSteps();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [providerType, connectorName]);

    useEffect(() => {
        if (!steps[currentStepIndex] || steps[currentStepIndex].type !== 'redirect' || !steps[currentStepIndex].polling_id) {
            setPolling(false);
            return;
        }

        const currentStep = steps[currentStepIndex];
        const pollingId = currentStep.polling_id;
        const targetUrl = currentStep.value;

        if (targetUrl) {
            window.open(targetUrl, '_blank', 'noopener,noreferrer');
        }

        setPolling(true);
        const pollInterval = setInterval(async () => {
            try {
                if (pollingId) {
                    const statusRes = await emailConnectors.getSetupStatus(pollingId);
                    if (statusRes.status === 'completed' || statusRes.status === 'success') {
                        setPolling(false);
                        clearInterval(pollInterval);
                        // Auto-advance
                        if (currentStepIndex < steps.length - 1) {
                            setCurrentStepIndex(currentStepIndex + 1);
                        } else {
                            navigate('/providers');
                        }
                    } else if (statusRes.status === 'error' || statusRes.status === 'failed') {
                        setPolling(false);
                        clearInterval(pollInterval);
                        setErrorMsg('Authorization failed or was rejected.');
                    }
                }
            } catch (err) {
                console.error('Polling error:', err);
                // Could be temporary network error, keep polling or abort if 404
            }
        }, 3000);

        return () => {
            clearInterval(pollInterval);
            setPolling(false);
        };
    }, [currentStepIndex, steps, navigate]);

    const loadSteps = async () => {
        if (!providerType) return;
        try {
            const fetchedSteps = await EmailConnectorFlow.startProviderSetup(providerType, connectorName);
            // Assuming startProviderSetup handles redirect step directly, so if it returns steps, we display them
            setSteps(fetchedSteps.map(s => ({...s, value: s.value || ''})));
        } catch (error) {
            console.error('Failed to start connector setup:', error);
            setErrorMsg('Failed to load setup steps.');
        } finally {
            setLoading(false);
        }
    };

    const handleStepChange = (value: string) => {
        setSteps(prev => {
            const next = [...prev];
            next[currentStepIndex].value = value;
            return next;
        });
    };

    const handleNext = async () => {
        setErrorMsg('');
        const currentStep = steps[currentStepIndex];

        if (currentStep.callback) {
            setSubmitting(true);
            try {
                // Send all steps up to current index
                const stepsToSend = steps.slice(0, currentStepIndex + 1);
                const path = `email-step-callback/${providerType}/${currentStep.callback}`;
                const response = await emailConnectors.runStepCallback(path, stepsToSend);

                if (response && !response.success) {
                    setErrorMsg(response.message || 'Validation failed.');
                    setSubmitting(false);
                    return;
                }
            } catch (error: unknown) {
                const reqError = error as { response?: { data?: { error?: string; message?: string } } };
                setErrorMsg(reqError.response?.data?.error || reqError.response?.data?.message || 'Failed step callback.');
                setSubmitting(false);
                return;
            }
            setSubmitting(false);
        }

        if (currentStepIndex < steps.length - 1) {
            setCurrentStepIndex(currentStepIndex + 1);
        } else {
            // Done
            navigate('/providers');
        }
    };

    const handleBack = () => {
        setErrorMsg('');
        if (currentStepIndex > 0) {
            setCurrentStepIndex(currentStepIndex - 1);
        } else {
            navigate('/providers');
        }
    };

    if (loading) {
        return (
            <Container maxWidth="sm">
                <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '50vh' }}>
                    <CircularProgress />
                </Box>
            </Container>
        );
    }

    if (steps.length === 0) {
        return (
            <Container maxWidth="sm">
                <Box sx={{ mt: 4 }}>
                    <Typography>No steps found or redirected.</Typography>
                    <Button onClick={() => navigate('/providers')}>Go Back</Button>
                </Box>
            </Container>
        );
    }

    const currentStep = steps[currentStepIndex];
    const isLastStep = currentStepIndex === steps.length - 1;

    return (
        <Container maxWidth="sm">
            <Box sx={{ mt: 4, mb: 4 }}>
                <Paper elevation={3} sx={{ p: 4 }}>
                    <Typography variant="h5" component="h1" gutterBottom>
                        Setup {providerType} Connector {connectorName ? `- ${connectorName}` : ''}
                    </Typography>
                    
                    <Typography variant="subtitle1" color="text.secondary" gutterBottom>
                        Step {currentStepIndex + 1} of {steps.length}
                    </Typography>
                    
                    <Box sx={{ my: 4 }}>
                        {currentStep.type === 'redirect' && (
                            <Stack spacing={2} alignItems="center">
                                <Typography variant="body1">{currentStep.desc || 'Please complete authorization in the new window.'}</Typography>
                                {currentStep.value && (
                                    <Button variant="contained" href={currentStep.value} target="_blank" rel="noopener noreferrer">
                                        {currentStep.title || 'Open Authorization Content'}
                                    </Button>
                                )}
                                {polling && (
                                    <>
                                        <CircularProgress size={40} sx={{ mt: 2 }} />
                                        <Typography variant="body2" color="text.secondary">Waiting for authorization to complete...</Typography>
                                    </>
                                )}
                            </Stack>
                        )}
                        {currentStep.type === 'input' && (
                            <TextField
                                label={currentStep.title}
                                helperText={currentStep.desc}
                                value={currentStep.value || ''}
                                onChange={(e) => handleStepChange(e.target.value)}
                                onKeyDown={(e) => {
                                    if (e.key === 'Enter' && !submitting) {
                                        e.preventDefault();
                                        handleNext();
                                    }
                                }}
                                fullWidth
                            />
                        )}
                        {currentStep.type === 'password' && (
                            <TextField
                                label={currentStep.title}
                                helperText={currentStep.desc}
                                type="password"
                                value={currentStep.value || ''}
                                onChange={(e) => handleStepChange(e.target.value)}
                                onKeyDown={(e) => {
                                    if (e.key === 'Enter' && !submitting) {
                                        e.preventDefault();
                                        handleNext();
                                    }
                                }}
                                fullWidth
                            />
                        )}
                        {currentStep.type === 'boolean' && (
                            <FormControlLabel
                                control={
                                    <Checkbox
                                        checked={currentStep.value === 'true'}
                                        onChange={(e) => handleStepChange(e.target.checked ? 'true' : 'false')}
                                    />
                                }
                                label={<>
                                    <Typography>{currentStep.title}</Typography>
                                    <Typography variant="caption" color="text.secondary">{currentStep.desc}</Typography>
                                </>}
                            />
                        )}
                    </Box>

                    {errorMsg && (
                        <Typography color="error" variant="body2" sx={{ mb: 2 }}>
                            {errorMsg}
                        </Typography>
                    )}

                    <Stack direction="row" spacing={2} justifyContent="space-between">
                        <Button
                            variant="outlined"
                            onClick={handleBack}
                            disabled={submitting}
                        >
                            {currentStepIndex === 0 ? 'Cancel' : 'Back'}
                        </Button>

                        {currentStep.type !== 'redirect' && (
                            <Button
                                variant="contained"
                                color="primary"
                                onClick={handleNext}
                                disabled={submitting}
                            >
                                {submitting ? 'Please wait...' : (isLastStep ? 'Submit' : 'Next')}
                            </Button>
                        )}
                    </Stack>
                </Paper>
            </Box>
        </Container>
    );
}



