export interface ConfirmationRaw {
    id: number,
    jsonPayload: string,
    edited: boolean
}

export interface Confirmation {
    id: number,
    jsonPayload: Record<string, string>,
    edited: boolean
}
