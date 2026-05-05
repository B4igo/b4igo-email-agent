"""Unit tests for the AI pipeline api."""

import io
from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock, patch

from docling.datamodel.accelerator_options import AcceleratorDevice, AcceleratorOptions
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from flask import Flask
from werkzeug.datastructures import FileStorage

import ai_service.app as api_module
from ai_service.app import (
    parse_text,
    parse_text_with_attachments,
)
from shared.attachment_utils import append_attachments_to_text

HERE = Path(__file__).resolve().parent

accelerator_options = AcceleratorOptions(num_threads=8, device=AcceleratorDevice.CPU)

pipeline_options = PdfPipelineOptions()
pipeline_options.accelerator_options = accelerator_options

app = Flask(__name__)


class TestParseText(TestCase):

    def setUp(self):
        self._enqueue_patcher = patch("ai_service.app.enqueue_confirmation")
        self._enqueue_patcher.start()

    def tearDown(self):
        self._enqueue_patcher.stop()

    def test_parse_text_returns_201_with_valid_text(self):
        with app.test_request_context(
            "/api/ai/text",
            method="POST",
            json={"text": "Meeting tomorrow at 3pm with Dr. Smith"},
            content_type="application/json",
        ):
            _, status = parse_text()

        self.assertEqual(status, 201)

    def test_parse_text_returns_400_when_text_missing(self):
        with app.test_request_context(
            "/api/ai/text",
            method="POST",
            json={},
            content_type="application/json",
        ):
            _, status = parse_text()

        self.assertEqual(status, 400)

    def test_parse_text_calls_pipeline_with_text(self):
        text = "Dentist appointment on Friday at 10am"
        with app.test_request_context(
            "/api/ai/text",
            method="POST",
            json={"text": text},
            content_type="application/json",
        ):
            spy = MagicMock(wraps=api_module.pipeline)
            with patch.object(api_module, "pipeline", spy):
                parse_text()

        spy.assert_called_once_with(text)

    def test_parse_text_returns_processed_status(self):
        with app.test_request_context(
            "/api/ai/text",
            method="POST",
            json={"text": "Some legal notice arrived"},
            content_type="application/json",
        ):
            response, _ = parse_text()

        data = response.get_json()
        self.assertEqual(data["status"], "processed")


class TestParseTextWithAttachments(TestCase):

    def setUp(self):
        self._enqueue_patcher = patch("ai_service.app.enqueue_confirmation")
        self._enqueue_patcher.start()

    def tearDown(self):
        self._enqueue_patcher.stop()

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_attachment_filepath = (
            HERE / "test_attachments" / "test_health.pdf"
        ).resolve()

    def test_returns_400_when_no_username_provided(self):
        with app.test_request_context(
            "/api/ai/text-with-attachments",
            method="POST",
            data={"text": "Some message"},
            content_type="multipart/form-data",
        ):
            _, status = parse_text_with_attachments()

        self.assertEqual(status, 400)

    def test_returns_201_with_valid_file(self):
        with open(self.test_attachment_filepath, "rb") as f:
            file_bytes = f.read()

        data = {
            "username": "testuser",
            "text": "See attached health document",
            "files": (io.BytesIO(file_bytes), "test_health.pdf"),
        }
        with app.test_request_context(
            "/api/ai/text-with-attachments",
            method="POST",
            data=data,
            content_type="multipart/form-data",
        ):
            _, status = parse_text_with_attachments()

        self.assertEqual(status, 201)

    def test_calls_pipeline_with_combined_text_and_attachment(self):
        with open(self.test_attachment_filepath, "rb") as f:
            file_bytes = f.read()

        data = {
            "username": "testuser",
            "text": "See attached",
            "files": (io.BytesIO(file_bytes), "test_health.pdf"),
        }
        with app.test_request_context(
            "/api/ai/text-with-attachments",
            method="POST",
            data=data,
            content_type="multipart/form-data",
        ):
            spy = MagicMock(wraps=api_module.pipeline)
            with patch.object(api_module, "pipeline", spy):
                parse_text_with_attachments()

        spy.assert_called_once()
        combined_text = spy.call_args[0][0]
        self.assertIn("See attached", combined_text)
        self.assertIn("Attachments:", combined_text)

    def test_text_defaults_to_empty_string_when_omitted(self):
        with open(self.test_attachment_filepath, "rb") as f:
            file_bytes = f.read()

        data = {
            "username": "testuser",
            "files": (io.BytesIO(file_bytes), "test_health.pdf"),
        }
        with app.test_request_context(
            "/api/ai/text-with-attachments",
            method="POST",
            data=data,
            content_type="multipart/form-data",
        ):
            _, status = parse_text_with_attachments()

        self.assertEqual(status, 201)


class TestAppendAttachmentsToText(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(
                    pipeline_options=pipeline_options,
                )
            }
        )
        cls.test_attachment_filepath = (
            HERE / "test_attachments" / "test_health.pdf"
        ).resolve()

    def test_attachment_conversion(self):
        text = "Hey, what's up!"

        with open(self.test_attachment_filepath, "rb") as fp:
            files = [FileStorage(fp)]
            result = append_attachments_to_text(files, text)

        self.assertIn(text, result)
        self.assertIn("Attachments:", result)

    def test_appending_attachments_includes_separator(self):
        with open(self.test_attachment_filepath, "rb") as fp:
            files = [FileStorage(fp)]
            result = append_attachments_to_text(files, "prefix text")

        self.assertIn("------------------", result)

    def test_appending_attachments_labels_attachment_index(self):
        with open(self.test_attachment_filepath, "rb") as fp:
            files = [FileStorage(fp)]
            result = append_attachments_to_text(files, "")

        self.assertIn("ATTACHMENT 0:", result)


if __name__ == "__main__":
    import unittest

    unittest.main()
