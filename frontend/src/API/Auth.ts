import axios from 'axios';
import { ec as EC } from 'elliptic';
import { computeAddress, Wallet } from 'ethers';

declare const chrome: any;

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:5000/api';

const api = axios.create({
    baseURL: BACKEND_URL,
});

api.interceptors.request.use((config) => {
    const token = localStorage.getItem('_auth');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        if ([401,422].includes(error.response?.status) && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                const data = await auth.performSiweFlow();
                originalRequest.headers.Authorization = `Bearer ${data.jwt}`;
                return api(originalRequest);
            } catch (reauthError) {
                localStorage.clear();
                window.location.href = '/login';
                return Promise.reject(reauthError);
            }
        }
        return Promise.reject(error);
    }
);


export const auth = {
    async init(address: string) {
        const { data } = await axios.post(`${BACKEND_URL}/auth/init`, {
            address
        });
        return data;
    },

    async performSiweFlow(signIn?: any) {
        let keysRaw = localStorage.getItem("allPrivateKeys");
        
        if (!keysRaw && typeof chrome !== 'undefined' && chrome.storage && chrome.storage.local) {
            const result = await new Promise<{ allPrivateKeys?: string }>((resolve) => {
                chrome.storage.local.get(['allPrivateKeys'], (res: any) => resolve(res as any));
            });
            keysRaw = result.allPrivateKeys || null;
        }

        if (!keysRaw) {
            throw new Error(
                "Authentication keys not found. Please ensure you are logged into the B4iGo website and navigate to it" +
                " for your keys to be transferred to the extension."
            );
        }

        let keys;
        try {
            keys = JSON.parse(keysRaw || "[]");
        } catch (e) {
            throw new Error("Failed to parse authentication keys. Please clear your storage and try again.");
        }

        const entry = keys.find((d: any) => d.isBackup === false);
        const pivKey = entry?.privateKey?.privateKeyHex;

        if (!pivKey) {
            throw new Error(
                "Active private key not found in stored keys. Please clear your storage and try again."
            );
        }

        const ec = new EC("secp256k1");
        const keyPair = ec.keyFromPrivate(pivKey, "hex");
        const publicKeyUncompressed = keyPair.getPublic().encode("hex", false);

        const publicKeyWithoutPrefix = publicKeyUncompressed.slice(2);
        const address = computeAddress("0x" + publicKeyWithoutPrefix);

        try {
            const { siweMessage, requestId } = await this.init(address);

            const wallet = new Wallet(pivKey);
            const signature = await wallet.signMessage(siweMessage);

            const { data } = await axios.post(`${BACKEND_URL}/auth/verify`, {
                signature,
                requestId
            });

            if (signIn) {
                signIn({
                    token: data.jwt,
                    expiresIn: 3600,
                    tokenType: 'Bearer',
                    authState: { userId: data.userId, email: data.email }
                });
            } else {
                localStorage.setItem('_auth', data.jwt);
            }

            return data;
        } catch (err: any) {
            console.error("SIWE flow error:", err);
            const msg = err.response?.data?.error || err.message || "Unknown authentication error";
            throw new Error(`Authentication failed: ${msg}`);
        }
    },

    async logout() {
        try {
            await api.post('/auth/logout');
        } finally {
            localStorage.clear();

            if (typeof chrome !== 'undefined' && chrome.storage?.local) {
                await new Promise<void>((resolve) => {
                    chrome.storage.local.remove(['allPrivateKeys'], () => resolve());
                });
            }
        }
    },
};

export { api };
