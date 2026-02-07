import {Box, Button, Card, Stack} from "@mui/material";

export default function NavBar({ children }: { children: React.ReactNode }) {
    return <>
        <Card sx={{ display: 'flex', justifyContent: 'space-between', boxShadow: 3 }}>
            <Button href="/" aria-label="home" sx={{ margin: 1 }}>
                <Box component="img" src="https://www.b4igo.com/B4iGo-logo.png" alt="home" sx={{ width: 164, height: 32 }} />
            </Button>
            <Stack direction="row">
                <Button href="/logout" variant="outlined" sx={{ margin: 1 }}>Logout</Button>
                <Button href="/providers" variant="outlined" sx={{ margin: 1 }}>Manage Email Providers</Button>
            </Stack>
        </Card>
        {children}
    </>
}