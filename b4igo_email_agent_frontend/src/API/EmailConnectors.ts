import { api } from "./Auth.ts";
import type { EmailConnector, EmailSetupStep } from "../Domain/EmailConnector.ts";

export const emailConnectors = {
    async getAll(): Promise<EmailConnector[]> {
        const { data } = await api.get<EmailConnector[]>('/email-connectors');
        return data;
    },

    async getTypes(): Promise<string[]> {
        const { data } = await api.get<string[]>('/email-connectors/types');
        return data;
    },

    async getSetupSteps(connectorType: string, connectorName?: string): Promise<EmailSetupStep[]> {
        const params = new URLSearchParams();
        if (connectorName) {
            params.set('name', connectorName);
        }
        const suffix = params.toString() ? `?${params.toString()}` : '';
        const { data } = await api.get<EmailSetupStep[]>(`/email-connectors/setup/${connectorType}${suffix}`);
        return data;
    },

    async remove(connectorId: number): Promise<void> {
        await api.delete(`/email-connectors/${connectorId}`);
    },

    async runStepCallback(callbackPath: string, steps: EmailSetupStep[]): Promise<{ success: boolean; message: string }> {
        const { data } = await api.post<{ success: boolean; message: string }>(callbackPath, { steps });
        return data;
    },
};