import {emailConnectors} from "../API/EmailConnectors.ts";

export class EmailConnectorFlow {
    static async startProviderSetup(provider: string, connectorName?: string): Promise<void> {
        console.log('Starting provider setup flow...', provider);

        const steps = await emailConnectors.getSetupSteps(provider, connectorName);
        console.log('Setup steps received:', steps);

        const redirectStep = steps.find(step => step.type === 'redirect');

        if (!redirectStep || !redirectStep.value) {
            throw new Error('No redirect step found for provider setup');
        }

        console.log('Redirecting to:', redirectStep.value);

        window.location.href = redirectStep.value;
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