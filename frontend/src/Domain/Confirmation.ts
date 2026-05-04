export interface ConfirmationRaw {
    id: number,
    jsonPayload?: string,
    json_payload?: string,
    edited?: boolean
}

export interface Confirmation {
    id: number,
    jsonPayload: Record<string, string>,
    edited: boolean
}
