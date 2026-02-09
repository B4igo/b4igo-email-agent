"""Tests for SchemaPrompter."""

import unittest

from b4igo_email_agent.ai_pipeline.schemas.schema_prompter import SchemaPrompter


class TestSchemaPrompter(unittest.TestCase):
    def test_health_prompt_is_string(self) -> None:
        prompter = SchemaPrompter()
        prompt = prompter.get_domain_prompt("health")

        self.assertIsInstance(prompt, str)
        self.assertTrue(prompt)


if __name__ == "__main__":
    unittest.main()
