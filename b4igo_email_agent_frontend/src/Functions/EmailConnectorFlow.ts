import {emailConnectors} from "../API/EmailConnectors.ts";

export class EmailConnectorFlow {
    static async startGmailOAuth(connectorName?: string): Promise<void> {
        console.log('Starting Gmail OAuth flow...');

        const steps = await emailConnectors.getSetupSteps('gmail');
        console.log('Setup steps received:', steps);

        const redirectStep = steps.find(step => step.type === 'redirect');

        if (!redirectStep) {
            console.error('No redirect step found in:', steps);
            throw new Error('No redirect step found for Gmail setup');
        }

        if (connectorName) {
            sessionStorage.setItem('gmail_connector_name', connectorName);
        }
        if (redirectStep.state) {
            sessionStorage.setItem('gmail_oauth_state', redirectStep.state);
        }

        console.log('Redirecting to:', redirectStep.value);

        window.location.href = redirectStep.value;
    }

    static async handleGmailCallback(): Promise<{ success: boolean; email?: string; error?: string }> {
        const urlParams = new URLSearchParams(window.location.search);
        const authCode = urlParams.get('code');
        const state = urlParams.get('state');
        const error = urlParams.get('error');

        if (error) {
            return { success: false, error: `OAuth error: ${error}` };
        }

        if (!authCode) {
            return { success: false, error: 'No authorization code received' };
        }

        try {
            const connectorName = sessionStorage.getItem('gmail_connector_name') || undefined;
            const storedState = sessionStorage.getItem('gmail_oauth_state') || undefined;

            sessionStorage.removeItem('gmail_connector_name');
            sessionStorage.removeItem('gmail_oauth_state');

            const result = await emailConnectors.completeGmailOAuth(authCode, connectorName, state || storedState);

            return {
                success: true,
                email: result.connector_email
            };
        } catch (err) {
            const errorMessage = err instanceof Error ? err.message : 'Failed to complete OAuth';
            return { success: false, error: errorMessage };
        }
    }
}