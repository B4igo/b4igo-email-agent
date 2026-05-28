import {emailConnectors} from "../API/EmailConnectors.ts";
import type {EmailSetupStep} from "../Domain/EmailConnector.ts";

export class EmailConnectorFlow {
    static async startProviderSetup(provider: string, connectorName?: string): Promise<EmailSetupStep[]> {
        const steps = await emailConnectors.getSetupSteps(provider, connectorName);
        return steps;
    }

    static async handleProviderCallback(): Promise<{ success: boolean; email?: string; error?: string }> {
        const urlParams = new URLSearchParams(window.location.search);
        const success = urlParams.get('success');
        const email = urlParams.get('email');
        const error = urlParams.get('error');

        if (success === '1') {
            return { success: true, email: email || undefined };
        }

        return {
            success: false,
            error: error || 'Failed to complete OAuth',
        };
    }
}