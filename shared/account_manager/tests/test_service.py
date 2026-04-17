"""Unit tests for AccountManagerService."""

import tempfile
from pathlib import Path
from unittest import TestCase

from shared.account_manager.providers import EmailProvider
from shared.account_manager.service import AccountManagerService
from shared.account_manager.storage import AccountStorage


class _FakeProvider(EmailProvider):
    """Deterministic provider for service tests."""

    def pull(self, account):
        """Return one fake email entry."""
        return [
            {
                "provider": account.provider,
                "accountId": account.id,
                "emailAddress": account.email_address,
                "subject": "fake",
                "body": "fake",
            }
        ]

    def GetSetup(self):
        return []

    def CallFunction(self, function_name, steps, account_id, storage):
        _ = function_name
        _ = steps
        return ""


class _FailingProvider(EmailProvider):
    """Provider that always fails for error-path tests."""

    def pull(self, account):
        """Raise an error on pull."""
        raise RuntimeError("pull failed")

    def GetSetup(self):
        return []

    def CallFunction(self, function_name, steps, account_id, storage):
        _ = function_name
        _ = steps
        return ""


class TestAccountManagerService(TestCase):
    """Unit tests for account manager orchestration behavior."""

    def setUp(self) -> None:
        """Create isolated storage and service per test."""
        self.tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.tmp.close()
        storage = AccountStorage(db_path=self.tmp.name)
        self.service = AccountManagerService(
            storage=storage,
            providers={"imap": _FakeProvider(), "gmail": _FailingProvider()},
        )

    def tearDown(self) -> None:
        """Delete temporary sqlite file."""
        Path(self.tmp.name).unlink(missing_ok=True)

    def test_link_account_redacts_sensitive_credentials(self) -> None:
        """link_account returns redacted credential fields in response."""
        linked = self.service.link_account(
            b4igo_user_id="u1",
            provider="imap",
            email_address="u@example.com",
            credentials={"username": "u", "password": "secret"},
        )
        self.assertIsNotNone(linked)
        assert linked is not None
        self.assertEqual(linked["credentials"]["username"], "u")
        self.assertEqual(linked["credentials"]["password"], "***")

    def test_pull_aggregates_emails_and_errors(self) -> None:
        """pull returns provider emails and provider errors together."""
        self.service.link_account(
            b4igo_user_id="u1",
            provider="imap",
            email_address="u@example.com",
            credentials={"password": "secret"},
        )
        self.service.link_account(
            b4igo_user_id="u1",
            provider="gmail",
            email_address="u@gmail.com",
            credentials={"access_token": "token"},
        )

        result = self.service.pull("u1")
        self.assertEqual(result["accountsPolled"], 2)
        self.assertEqual(len(result["emails"]), 1)
        self.assertEqual(len(result["errors"]), 1)
        self.assertEqual(result["errors"][0]["error"], "pull failed")

    def test_delete_account(self) -> None:
        """delete_account deletes row for user."""
        linked = self.service.link_account(
            b4igo_user_id="u1",
            provider="imap",
            email_address="u@example.com",
            credentials={"password": "secret"},
        )
        assert linked is not None
        self.assertTrue(self.service.delete_account("u1", linked["id"]))
        self.assertFalse(self.service.delete_account("u1", linked["id"]))

    def test_seed_and_authenticate_user(self) -> None:
        """seed_user creates auth user and authenticate_user validates credentials."""
        seeded = self.service.seed_user("user", "password", "user")
        self.assertEqual(seeded["username"], "user")
        self.assertTrue(self.service.user_exists("user"))

        auth_ok = self.service.authenticate_user("user", "password")
        self.assertIsNotNone(auth_ok)
        auth_fail = self.service.authenticate_user("user", "bad")
        self.assertIsNone(auth_fail)
