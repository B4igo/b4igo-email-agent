import {api} from "./Auth.ts";

import type {Confirmation, ConfirmationRaw} from "../Domain/Confirmation.ts";

export const confirmations = {
    async getAll() {
        const { data } = await api.get<ConfirmationRaw[]>('/confirmations')
        return data.map(conf => ({
            ...conf,
            jsonPayload: JSON.parse(conf.jsonPayload)
        })) as Confirmation[];
    },

    async reject(id: number) {
        await api.post(`/reject-confirmation`, { id });
    },

    async accept(id: number, jsonPayload: Record<string, string> | undefined = undefined) {
        await api.post(`/accept-confirmation`,
            jsonPayload ? { id, jsonPayload } : { id });
    },
};
