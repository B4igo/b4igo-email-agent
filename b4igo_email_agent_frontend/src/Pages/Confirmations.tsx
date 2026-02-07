import {Box, Button, Card, CardContent, CircularProgress, Stack, TextField, Typography} from "@mui/material";
import {useState} from "react";
import {confirmations} from "../API/Confirmations.ts";
import {useRepeatingFetch} from "../Functions/Helpers.ts";
import type {Confirmation} from "../Domain/Confirmation.ts";

export const Confirmations = () => {

    const [Confirmations, SetConfirmations] = useState<Confirmation[] | undefined>(undefined);

    useRepeatingFetch(confirmations.getAll, SetConfirmations, 10000)

    return <Box sx={{ m: 2 }}>
        {!Confirmations && <Box display="flex" justifyContent="center">
            <CircularProgress />
        </Box>}
        {Confirmations && <Stack
            direction="column"
            spacing={2}
            sx={{ overflowX: 'auto', pb: 2 }}
        >
            {Confirmations.map((confirmation, i) => (
                <Card key={confirmation.id} sx={{ minWidth: 350, display: 'flex', flexDirection: 'column', boxShadow: 3 }} variant="outlined">
                    <CardContent sx={{ flexGrow: 1 }}>
                        <Typography variant="h6" noWrap>Email Confirmation</Typography>
                        <Stack direction="column" spacing={2} sx={{ mt: 2 }}>
                            {confirmation.jsonPayload && Object.entries(confirmation.jsonPayload).map(([key, value], j) => (
                                <TextField
                                    key={j}
                                    label={key}
                                    value={value}
                                    size="small"
                                    fullWidth
                                    onChange={(e) => {
                                        const updated = [...Confirmations];
                                        updated[i].jsonPayload[key] = e.target.value;
                                        updated[i].edited = true;
                                        SetConfirmations(updated);
                                    }}
                                />
                            ))}
                        </Stack>
                    </CardContent>

                    <Stack direction="row" spacing={1} sx={{ p: 2, pt: 0 }}>
                        <Button
                            fullWidth
                            variant="outlined"
                            color="error"
                            onClick={
                                () => confirmations
                                    .reject(confirmation.id)
                                    .then(() => SetConfirmations(Confirmations.filter(c => c.id !== confirmation.id)))
                                    .catch(console.error)
                            }
                        >
                            Reject
                        </Button>
                        <Button
                            fullWidth
                            variant="contained"
                            onClick={() => confirmations
                                .accept(confirmation.id, confirmation.edited ? confirmation.jsonPayload : undefined)
                                .then(() => SetConfirmations(Confirmations.filter(c => c.id !== confirmation.id)))
                                .catch(console.error)
                            }
                        >
                            Add to Vault
                        </Button>
                    </Stack>
                </Card>
            ))}
        </Stack>
        }
    </Box>
}