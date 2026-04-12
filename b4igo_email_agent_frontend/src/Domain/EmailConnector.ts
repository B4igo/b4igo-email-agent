export interface EmailConnector {
    id: number;
    connector_type: string;
    connector_name: string;
    connector_email: string;
    has_token: boolean;
    last_read: string | null;
    last_error_msg: string | null;
}

export interface EmailSetupStep {
    title: string;
    desc: string;
    type: 'redirect' | 'boolean' | 'input' | 'password';
    value?: string;
    callback?: string;
    polling_id?: string;
}
