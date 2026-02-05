import {api} from "./Auth.ts";

import type {Confirmation} from "../Domain/Confirmation.ts";

export const confirmations = {
    async getAll() {
        const { data } = await api.get<Confirmation[]>('/confirmations');
        return data;
    },
};
