import {Box, Button, Card, Stack} from "@mui/material";

export default function NavBar({ children }: { children: React.ReactNode }) {
    const handleFileSelect = async (
        event: React.ChangeEvent<HTMLInputElement>
    ) => {
        const file = event.target.files?.[0];
        if (!file) return;

        //const formData = new FormData();
        //formData.append("file", file);

        //TODO api request via a function

        event.target.value = "";
    };

    return <>
        <Card sx={{ display: 'flex', justifyContent: 'space-between', boxShadow: 3 }}>
            <Button href="/" aria-label="home" sx={{ margin: 1 }}>
                <Box component="img" src="https://www.b4igo.com/B4iGo-logo.png" alt="home" sx={{ width: 164, height: 32 }} />
            </Button>
            <Stack direction="row">
                <Button variant="outlined" component="label" sx={{ margin: 1 }}>
                    Upload File
                    <input hidden type="file" onChange={handleFileSelect} />
                </Button>
                <Button href="/logout" variant="contained" sx={{ margin: 1 }}>Logout</Button>
                <Button href="/email-connectors" variant="contained" sx={{ margin: 1 }}>Manage Email Providers</Button>
            </Stack>
        </Card>
        {children}
    </>
}