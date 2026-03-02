import { api } from "./Auth.ts";
import type { EmailConnector, EmailSetupStep, AddConnectorResponse } from "../Domain/EmailConnector.ts";

export const emailConnectors = {
    async getAll(): Promise<EmailConnector[]> {
        const { data } = await api.get<EmailConnector[]>('/email-connectors');
        return data;
    },

    async getTypes(): Promise<string[]> {
        const { data } = await api.get<string[]>('/email-connectors/types');
        return data;
    },

    async getSetupSteps(connectorType: string): Promise<EmailSetupStep[]> {
        const { data } = await api.get<EmailSetupStep[]>(`/email-connectors/setup/${connectorType}`);
        return data;
    },

    async remove(connectorId: number): Promise<void> {
        await api.delete(`/email-connectors/${connectorId}`);
    },

    async addGmailManual(connectorName: string, tokenJson: string): Promise<AddConnectorResponse> {
        const { data } = await api.post<AddConnectorResponse>('/email-connectors/gmail/add', {
            connector_name: connectorName,
            token_json: tokenJson
        });
        return data;
    },

    async completeGmailOAuth(authCode: string, connectorName?: string, state?: string): Promise<AddConnectorResponse> {
        const params = new URLSearchParams({ code: authCode });
        if (connectorName) {
            params.append('name', connectorName);
        }
        if (state) {
            params.append('state', state);
        }

        const { data } = await api.get<AddConnectorResponse>(
            `/email-connectors/gmail/callback?${params.toString()}`
        );
        return data;
    }
};