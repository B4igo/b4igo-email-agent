import {Box} from "@mui/material";
import {useState} from "react";
import {confirmations} from "../API/Confirmations.ts";
import {useRepeatingFetch} from "../Functions/Helpers.ts";

export const Confirmations = () => {

    const [Confirmations, SetConfirmations] = useState([]);

    useRepeatingFetch(confirmations.getAll, SetConfirmations, 10000)

    return <Box>{Confirmations.toString()}</Box>
}