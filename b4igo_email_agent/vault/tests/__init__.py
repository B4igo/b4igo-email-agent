"""Tests for vault module."""

import unittest


def load_tests(loader, standard_tests, pattern):
    """Load all test_*.py modules in this package so 'unittest vault.tests' runs them."""
    suite = unittest.TestSuite()
    suite.addTests(
        loader.loadTestsFromName("b4igo_email_agent.vault.tests.test_vault_client")
    )
    suite.addTests(
        loader.loadTestsFromName("b4igo_email_agent.vault.tests.test_vault_storage")
    )
    return suite
