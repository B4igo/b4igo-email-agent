import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom"
import Login from "./Pages/Login.tsx"
import { AuthProvider, RequireAuth } from 'react-auth-kit'
import {Confirmations} from "./Pages/Confirmations.tsx";
import Logout from "./Pages/Logout.tsx";
import NavBar from "./Components/NavBar.tsx";
import {EmailConnectorsPage} from "./Pages/EmailConnectors.tsx";
import {ProviderCallbackPage} from "./Pages/Callback.tsx";
import {SetupConnectorPage} from "./Pages/SetupConnector.tsx";
import UploadFiles from "./Pages/UploadFiles.tsx";

ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
        <AuthProvider
            authType="localstorage"
            authName="_auth"
            cookieDomain={window.location.hostname}
            cookieSecure={window.location.protocol === 'https:'}
        >
            <BrowserRouter>
                <Routes>
                    <Route path="/login" element={<Login />} />
                    <Route
                        path="/*"
                        element={
                            <RequireAuth loginPath="/login">
                                <NavBar>
                                    <Routes>
                                        <Route path="/" element={<Confirmations/>} />
                                        <Route path="/upload" element={<UploadFiles/>} />
                                        <Route path="/email-connectors/callback" element={<ProviderCallbackPage/>} />
                                        <Route path="/email-connectors" element={<EmailConnectorsPage/>} />
                                        <Route path="/logout" element={<Logout />} />
                                        <Route path="/providers" element={<EmailConnectorsPage/>} />
                                        <Route path="/providers/setup/:providerType" element={<SetupConnectorPage/>} />
                                        <Route path="*" element={<Navigate to="/" replace />} />
                                    </Routes>
                                </NavBar>
                            </RequireAuth>
                        }
                    />
                </Routes>
            </BrowserRouter>
        </AuthProvider>
    </React.StrictMode>,
)
