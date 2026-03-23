"""Unit tests for AccountStorage."""

import tempfile
from pathlib import Path
from unittest import TestCase

from b4igo_email_agent.account_manager.storage import AccountStorage


class TestAccountStorage(TestCase):
    """Unit tests for AccountStorage CRUD and filtering."""

    def setUp(self) -> None:
        """Create isolated sqlite file for each test."""
        self.tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.tmp.close()
        self.storage = AccountStorage(db_path=self.tmp.name)

    def tearDown(self) -> None:
        """Delete temporary sqlite file."""
        Path(self.tmp.name).unlink(missing_ok=True)

    def test_upsert_and_list_account(self) -> None:
        """upsert_account persists account and list_accounts returns it."""
        account = self.storage.upsert_account(
            b4igo_user_id="u1",
            provider="imap",
            email_address="user@example.com",
            credentials={"password": "x"},
            display_name="Primary",
        )
        self.assertIsNotNone(account)
        listed = self.storage.list_accounts("u1")
        self.assertEqual(len(listed), 1)
        self.assertEqual(listed[0].email_address, "user@example.com")
        self.assertEqual(listed[0].provider, "imap")

    def test_upsert_updates_existing_unique_account(self) -> None:
        """upsert_account updates by unique user/provider/email tuple."""
        account_1 = self.storage.upsert_account(
            b4igo_user_id="u1",
            provider="gmail",
            email_address="user@gmail.com",
            credentials={"refresh_token": "old"},
        )
        self.assertIsNotNone(account_1)

        account_2 = self.storage.upsert_account(
            b4igo_user_id="u1",
            provider="gmail",
            email_address="user@gmail.com",
            credentials={"refresh_token": "new"},
            display_name="Google",
        )
        self.assertIsNotNone(account_2)
        self.assertEqual(account_1.id, account_2.id)
        self.assertEqual(account_2.display_name, "Google")
        self.assertEqual(account_2.credentials["refresh_token"], "new")

    def test_get_accounts_by_ids(self) -> None:
        """get_accounts_by_ids filters to requested account ids."""
        a1 = self.storage.upsert_account(
            b4igo_user_id="u1",
            provider="imap",
            email_address="a@example.com",
            credentials={"password": "a"},
        )
        a2 = self.storage.upsert_account(
            b4igo_user_id="u1",
            provider="gmail",
            email_address="b@gmail.com",
            credentials={"access_token": "b"},
        )
        assert a1 is not None
        assert a2 is not None

        only_second = self.storage.get_accounts_by_ids("u1", [a2.id])
        self.assertEqual(len(only_second), 1)
        self.assertEqual(only_second[0].id, a2.id)

    def test_delete_account(self) -> None:
        """delete_account removes row and returns True."""
        account = self.storage.upsert_account(
            b4igo_user_id="u1",
            provider="imap",
            email_address="a@example.com",
            credentials={"password": "a"},
        )
        assert account is not None
        self.assertTrue(self.storage.delete_account("u1", account.id))
        self.assertEqual(self.storage.list_accounts("u1"), [])
        self.assertFalse(self.storage.delete_account("u1", account.id))
