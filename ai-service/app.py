"""Defines flask api for AI pipeline microservice"""

import os
import tempfile
from typing import Tuple

from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.accelerator_options import AcceleratorDevice, AcceleratorOptions
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
)
from flask import Flask, Response, jsonify, request
from pydantic import BaseModel
import requests
from werkzeug.datastructures import FileStorage

from shared.ai_pipeline.ai_pipeline import AIPipeline

FlaskResponse = Tuple[Response, int]
"""Response and error code"""

accelerator_options = AcceleratorOptions(num_threads=8, device=AcceleratorDevice.CPU)

pipeline_options = PdfPipelineOptions()
pipeline_options.accelerator_options = accelerator_options

# TODO: GPU processing is not working on my (Jake's) machine for some reason
# this uses cpu instead
converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(
            pipeline_options=pipeline_options,
        )
    }
)

# TODO: Will need to be changed when hooked up
pipeline = AIPipeline()
url = "http://localhost:5000/api/confirmations/enqueue"

app = Flask(__name__)


@app.route("/api/ai/text", methods=["POST"])
def parse_text() -> FlaskResponse:
    """Process text-only json message.

    Returns
    -------
    FlaskResponse
        Status.
    """
    payload = request.get_json()
    text = payload.get("text")
    username = payload.get("username", "user")

    if not username:
        return jsonify({"error": "No username provided"}), 400
    if not text:
        return jsonify({"error": "No text provided"}), 400

    entries = pipeline(text)
    # TODO: This is a test method, needs to be replaced with real user
    # to integrate
    _enqueue_entries(entries, username)

    return (
        jsonify(
            {
                "status": "processed",
            }
        ),
        201,
    )


@app.route("/api/ai/text-with-attachments", methods=["POST"])
def parse_text_with_attachments() -> FlaskResponse:
    """Process multi-part form message with attachments.

    Returns
    -------
    FlaskResponse
        Status.
    """
    text = request.form.get("text")
    username = request.form.get("username", "user")
    files: list[FileStorage] = request.files.getlist("files")

    if not text:
        text = ""
    if not username:
        return jsonify({"error": "No username provided"}), 400
    if not files:
        return jsonify({"error": "No files provided"}), 400

    text = _append_attachments_to_text(files, text)
    entries = pipeline(text)
    # TODO: This is a test method, needs to be replaced with real user
    # to integrate
    _enqueue_entries(entries, username)

    return jsonify({"status": "processed"}), 202


def _enqueue_entries(entries: list[BaseModel], username: str):
    """Send entries to confirmation queue."""
    for entry in entries:
        payload = {"username": username, "jsonPayload": entry.model_dump_json()}
        response = requests.post(url, json=payload)
        print(response)


def _append_attachments_to_text(files: list[FileStorage], text: str) -> str:
    text += "\n\nAttachments: \n------------------\n\n"
    text += _convert_attachments_to_text(files)
    return text


def _convert_attachments_to_text(files: list[FileStorage]) -> str:
    text = ""
    for i, f in enumerate(files):
        ext = os.path.splitext(f.filename or "")[1]
        with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
            f.save(tmp.name)
            tmp_path = tmp.name
        try:
            result = converter.convert(tmp_path)
            text += f"ATTACHMENT {i}: \n"
            text += result.document.export_to_markdown()
            text += "\n"
        finally:
            os.remove(tmp_path)
    return text


if __name__ == "__main__":
    app.run(debug=True)
