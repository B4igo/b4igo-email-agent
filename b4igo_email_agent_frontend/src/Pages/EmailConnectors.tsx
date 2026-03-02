import {useEffect, useState} from "react";
import {
    Box,
    Button,
    Container,
    Typography,
    Paper,
    List,
    ListItem,
    ListItemText,
    CircularProgress,
    Chip,
    Stack,
    Divider,
    TextField
} from '@mui/material';
import type {EmailConnector} from "../Domain/EmailConnector.ts";
import {emailConnectors} from "../API/EmailConnectors.ts";
import {EmailConnectorFlow} from "../Functions/EmailConnectorFlow.ts";

export function EmailConnectorsPage() {
    const [connectors, setConnectors] = useState<EmailConnector[]>([]);
    const [loading, setLoading] = useState(true);
    const [connectorName, setConnectorName] = useState('');

    useEffect(() => {
        loadConnectors();
    }, []);

    const loadConnectors = async () => {
        try {
            const data = await emailConnectors.getAll();
            setConnectors(data);
        } catch (error) {
            console.error('Failed to load connectors:', error);
        } finally {
            setLoading(false);
        }
    };

    const isDuplicateName = (name: string): boolean => {
        return connectors.some(c => c.connector_name.toLowerCase() === name.toLowerCase());
    };

    const isAddButtonDisabled = (): boolean => {
        return connectorName.trim() === '' || isDuplicateName(connectorName.trim());
    };

    const handleAddGmail = async () => {
        try {
            await EmailConnectorFlow.startGmailOAuth(connectorName.trim());
        } catch (error) {
            console.error('Failed to start Gmail OAuth:', error);
        }
    };

    const handleRemove = async (id: number) => {
        try {
            await emailConnectors.remove(id);
            await loadConnectors();
        } catch (error) {
            console.error('Failed to remove connector:', error);
        }
    };

    if (loading) {
        return (
            <Container maxWidth="md">
                <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '50vh' }}>
                    <CircularProgress />
                </Box>
            </Container>
        );
    }

    return (
        <Container maxWidth="md">
            <Box sx={{ mt: 4, mb: 4 }}>
                <Stack spacing={3}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <Typography variant="h4" component="h1">
                            Email Connectors
                        </Typography>
                    </Box>

                    <Paper elevation={2}>
                        <List sx={{ p: 0 }}>
                            {connectors.map((connector, index) => (
                                <Box key={connector.id}>
                                    <ListItem
                                        sx={{ py: 2 }}
                                        secondaryAction={
                                            <Button
                                                variant="outlined"
                                                color="error"
                                                size="small"
                                                onClick={() => handleRemove(connector.id)}
                                            >
                                                Remove
                                            </Button>
                                        }
                                    >
                                        <ListItemText
                                            primary={
                                                <Typography variant="h6" component="div">
                                                    {connector.connector_name}
                                                </Typography>
                                            }
                                            secondary={
                                                <Stack spacing={1} sx={{ mt: 1 }}>
                                                    <Typography variant="body2" color="text.secondary">
                                                        {connector.connector_email}
                                                    </Typography>
                                                    {connector.last_error_msg && (
                                                        <Chip
                                                            label={`Error: ${connector.last_error_msg}`}
                                                            color="error"
                                                            size="small"
                                                            sx={{ alignSelf: 'flex-start' }}
                                                        />
                                                    )}
                                                </Stack>
                                            }
                                        />
                                    </ListItem>
                                    {index < connectors.length - 1 && <Divider />}
                                </Box>
                            ))}
                        </List>
                    </Paper>

                    <Paper>
                        <Stack spacing={1} sx={{ p: 1 }}>
                            <Typography variant="h6" component="h1">
                                Add Email Connector:
                            </Typography>

                            <TextField
                                label="Connector Name"
                                variant="outlined"
                                value={connectorName}
                                onChange={(e) => setConnectorName(e.target.value)}
                                error={connectorName.trim() !== '' && isDuplicateName(connectorName.trim())}
                                helperText={
                                    connectorName.trim() !== '' && isDuplicateName(connectorName.trim())
                                        ? 'A connector with this name already exists'
                                        : ''
                                }
                                fullWidth
                            />
                            <Stack spacing={1} direction="row" justifyContent="flex-end">
                                <Button
                                    variant="contained"
                                    color="primary"
                                    onClick={handleAddGmail}
                                    size="large"
                                    disabled={isAddButtonDisabled()}>
                                    Add Gmail
                                </Button>
                            </Stack>
                        </Stack>
                    </Paper>
                </Stack>
            </Box>
        </Container>
    );
}