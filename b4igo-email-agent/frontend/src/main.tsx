import React from 'react'
import ReactDOM from 'react-dom/client'
import {
    Box, Button, Card, Stack,

} from '@mui/material'
import { BrowserRouter, Route, Routes } from "react-router-dom"

ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
        <BrowserRouter>
            <Card sx={{ display: 'flex', justifyContent: 'space-between', boxShadow: 3 }}>
                <Button href="/" aria-label="home" sx={{margin: 1}}>
                    <Box component="img" src="https://www.b4igo.com/B4iGo-logo.png" alt="home" sx={{ width: 164, height: 32 }} />
                </Button>
                <Stack direction="row">
                    <Button href="/logout" variant="outlined" sx={{margin: 1}}>Logout</Button>
                    <Button href="/providers" variant="outlined" sx={{margin: 1}}>Manage Email Providers</Button>
                </Stack>
            </Card>

            <Routes>
                <Route path="/" element={<Box>TODO home page with email confirmations</Box>} />
                <Route path="/providers" element={<Box>TODO email providers page</Box>} />
                <Route path="/logout" element={<Box>TODO logout page</Box>} />
            </Routes>
        </BrowserRouter>
    </React.StrictMode>,
)