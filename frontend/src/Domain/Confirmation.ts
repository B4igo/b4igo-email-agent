export interface ConfirmationRaw {
    id: number,
    jsonPayload?: string,
    json_payload?: string,
    schemaName?: string,
    schema_name?: string,
    edited: boolean
}

export interface Confirmation {
    id: number,
    jsonPayload: Record<string, string>,
    schemaName: string,
    edited: boolean
}
