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

    def _headers(self) -> dict[str, str]:
        """Create headers for internal service calls."""
        headers = {"Content-Type": "application/json"}
        if self.service_token:
            headers["X-Internal-Service-Token"] = self.service_token
        return headers
