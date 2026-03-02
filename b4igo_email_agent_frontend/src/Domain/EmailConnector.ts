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
    type: 'redirect' | 'entry' | 'boolean';
    title: string;
    desc: string;
    callback: string;
    value: string;
    state?: string;
}

export interface AddConnectorResponse {
    message: string;
    id: number;
    connector_email: string;
}