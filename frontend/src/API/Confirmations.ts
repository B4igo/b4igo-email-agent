import {api} from "./Auth.ts";

import type {Confirmation, ConfirmationRaw} from "../Domain/Confirmation.ts";

export const confirmations = {
    async getAll() {
        const { data } = await api.get<ConfirmationRaw[]>('/confirmations')
        return data.map((conf) => {
            const rawPayload = conf.jsonPayload ?? conf.json_payload ?? "{}";
            let parsed: Record<string, string> = {};
            try {
                parsed = typeof rawPayload === "string" ? JSON.parse(rawPayload) : (rawPayload as Record<string, string>);
            } catch (error) {
                console.error("Failed to parse confirmation payload", error);
            }

            return {
                id: conf.id,
                jsonPayload: parsed,
                schemaName: conf.schemaName ?? conf.schema_name ?? "Unknown",
                edited: conf.edited ?? false
            } as Confirmation;
        });
    },

    async reject(id: number) {
        await api.post(`/reject-confirmation`, { id });
    },

    async accept(id: number, schemaName: string, jsonPayload: Record<string, string> | undefined = undefined) {
        await api.post(`/accept-confirmation`,
            jsonPayload ? { id, schemaName, jsonPayload } : { id, schemaName });
    },
};
