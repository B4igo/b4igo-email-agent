"""HTTP client used by middleware to call AccountManager microservice."""

import os
from typing import Any, Optional

import requests


class AccountManagerClient:
    """Client wrapper around internal AccountManager HTTP endpoints."""

    def __init__(self, base_url: Optional[str] = None, timeout_seconds: int = 10):
        """Initialize account manager client.

        Args:
            base_url: Internal account manager base URL.
            timeout_seconds: HTTP timeout applied to all requests.
        """
        self.base_url = (
            base_url
            or os.environ.get("B4IGO_ACCOUNT_MANAGER_URL")
            or "http://127.0.0.1:5100"
        ).rstrip("/")
        self.timeout_seconds = timeout_seconds
        self.service_token = os.environ.get("B4IGO_ACCOUNT_MANAGER_TOKEN")

    def link_account(
        self,
        b4igo_user_id: str,
        provider: str,
        email_address: str,
        credentials: dict[str, Any],
        display_name: Optional[str] = None,
        config: Optional[dict[str, Any]] = None,
    ) -> requests.Response:
        """Create or update linked account in AccountManager service."""
        payload: dict[str, Any] = {
            "b4igoUserId": b4igo_user_id,
            "provider": provider,
            "emailAddress": email_address,
            "credentials": credentials,
        }
        if display_name is not None:
            payload["displayName"] = display_name
        if config is not None:
            payload["config"] = config

        return requests.post(
            f"{self.base_url}/api/accounts/link",
            json=payload,
            headers=self._headers(),
            timeout=self.timeout_seconds,
        )

    def seed_user(
        self,
        username: str,
        password: str,
        role: str = "user",
    ) -> requests.Response:
        """Create or update one user in account-manager auth storage."""
        payload = {
            "username": username,
            "password": password,
            "role": role,
        }
        return requests.post(
            f"{self.base_url}/api/auth/seed-user",
            json=payload,
            headers=self._headers(),
            timeout=self.timeout_seconds,
        )

    def verify_user(self, username: str, password: str) -> requests.Response:
        """Verify username/password against account-manager auth storage."""
        payload = {
            "username": username,
            "password": password,
        }
        return requests.post(
            f"{self.base_url}/api/auth/verify",
            json=payload,
            headers=self._headers(),
            timeout=self.timeout_seconds,
        )

    def user_exists(self, username: str) -> requests.Response:
        """Check whether username exists in account-manager auth storage."""
        return requests.get(
            f"{self.base_url}/api/auth/users/{username}/exists",
            headers=self._headers(),
            timeout=self.timeout_seconds,
        )

    def list_accounts(self, b4igo_user_id: str) -> requests.Response:
        """List linked accounts for one user from AccountManager service."""
        return requests.get(
            f"{self.base_url}/api/accounts/{b4igo_user_id}",
            headers=self._headers(),
            timeout=self.timeout_seconds,
        )

    def delete_account(self, b4igo_user_id: str, account_id: int) -> requests.Response:
        """Delete one linked account from AccountManager service."""
        return requests.delete(
            f"{self.base_url}/api/accounts/{b4igo_user_id}/{account_id}",
            headers=self._headers(),
            timeout=self.timeout_seconds,
        )

    def list_provider_types(self) -> requests.Response:
        """List provider types available for setup."""
        return requests.get(
            f"{self.base_url}/api/providers/types",
            headers=self._headers(),
            timeout=self.timeout_seconds,
        )

    def get_provider_setup(
        self,
        provider: str,
        b4igo_user_id: str,
        connector_name: Optional[str] = None,
    ) -> requests.Response:
        """Fetch setup steps required to link a new provider account.

        Args:
            provider: Target provider (e.g. 'gmail').
            b4igo_user_id: B4iGO user identifier.
            connector_name: Optional explicit display name for account.

        Returns:
            List of setup step definitions or validation error.
        """
        payload = {
            "b4igoUserId": b4igo_user_id,
            "connectorName": connector_name,
        }
        return requests.post(
            f"{self.base_url}/api/providers/{provider}/setup",
            headers=self._headers(),
            json=payload,
            timeout=self.timeout_seconds,
        )

    def run_provider_step_callback(
        self,
        provider: str,
        function_name: str,
        steps: list[dict[str, Any]],
        b4igo_user_id: str,
    ) -> requests.Response:
        """Run one provider setup callback with raw steps payload."""
        payload = {
            "steps": steps,
            "b4igoUserId": b4igo_user_id,
        }
        return requests.post(
            f"{self.base_url}/api/providers/{provider}/steps/{function_name}",
            json=payload,
            headers=self._headers(),
            timeout=self.timeout_seconds,
        )

    def complete_provider_oauth(
        self,
        provider: str,
        auth_code: str,
        state: str,
        oauth_callback_url: str,
    ) -> requests.Response:
        """Complete provider OAuth callback and upsert the linked account."""
        payload = {
            "code": auth_code,
            "state": state,
            "oauthCallbackUrl": oauth_callback_url,
        }
        return requests.post(
            f"{self.base_url}/api/providers/{provider}/oauth/callback",
            json=payload,
            headers=self._headers(),
            timeout=self.timeout_seconds,
        )

    def _headers(self) -> dict[str, str]:
        """Create headers for internal service calls."""
        headers = {"Content-Type": "application/json"}
        if self.service_token:
            headers["X-Internal-Service-Token"] = self.service_token
        return headers
