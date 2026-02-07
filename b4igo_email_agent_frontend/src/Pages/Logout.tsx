import {useNavigate} from "react-router-dom";
import {useSignOut} from "react-auth-kit";
import React from "react";
import {auth} from "../API/Auth.ts";
import {Box} from "@mui/material";

export default function Logout() {
    const navigate = useNavigate()
    const signOut = useSignOut()

    React.useEffect(() => {
        auth.logout().finally(() => {
            signOut()
            navigate('/login')
        })
    }, [navigate, signOut])

    return <Box>Logging out...</Box>
}