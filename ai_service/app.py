"""Defines flask api for AI pipeline microservice."""

import logging
import os
import sys
import tempfile
from typing import Tuple

import requests
from docling.datamodel.accelerator_options import AcceleratorDevice, AcceleratorOptions
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from flask import Flask, Response, jsonify, request
from werkzeug.datastructures import FileStorage

from ai_service.ai_pipeline.ai_pipeline import AIPipeline

FlaskResponse = Tuple[Response, int]
"""Response and error code"""

accelerator_options = AcceleratorOptions(num_threads=8, device=AcceleratorDevice.CPU)

pipeline_options = PdfPipelineOptions()
pipeline_options.accelerator_options = accelerator_options

# TODO: GPU processing is not working on my (Jake's) machine for some reason
# this uses cpu instead
# TODO: Do you need to specify cpu for each input type?
converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(
            pipeline_options=pipeline_options,
        )
    }
)

# TODO: Will need to be changed when hooked up
reranker_model = os.environ.get("RERANKER_MODEL", None)
parser_model = os.environ.get("PARSER_MODEL", None)
pipeline = AIPipeline(reranker_model=reranker_model, parser_model=parser_model)
BACKEND_URL = os.environ.get("BACKEND_URL", "http://backend:5000").rstrip("/")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("ai-service")

app = Flask(__name__)


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


def enqueue_confirmation(username: str, payload: str):
    """POST a confirmation to the backend API."""
    resp = requests.post(
        f"{BACKEND_URL}/api/confirmations/enqueue",
        json={"user_id": username, "jsonPayload": payload},
        timeout=30,
    )
    if resp.status_code == 201:
        logger.info("enqueued confirmation for user %s", username)
    else:
        logger.warning(
            "failed to enqueue confirmation: status %s body %s",
            resp.status_code,
            resp.text,
        )


@app.route("/api/ai/text", methods=["POST"])
def parse_text() -> FlaskResponse:
    """Process text-only json message.

    Calls AI pipeline on passed text and enqueues entries in confirmation
    queue. If ``dry_run`` is true (body field or ``?dry_run=1`` query), the
    parsed entries are returned without being enqueued — used by the admin
    panel's AI playground.

    Returns
    -------
    FlaskResponse
        Status, or {"entries": [...]} when dry_run.
    """
    payload = request.get_json()
    text = payload.get("text")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    dry_run = bool(payload.get("dry_run")) or request.args.get("dry_run") in (
        "1",
        "true",
    )

    entries = pipeline(text)
    if dry_run:
        return (
            jsonify({"entries": [entry.model_dump(mode="json") for entry in entries]}),
            200,
        )

    for entry in entries:
        enqueue_confirmation(payload.get("username"), entry.model_dump_json())

    return (
        jsonify({"status": "processed"}),
        201,
    )


@app.route("/api/ai/text-with-attachments", methods=["POST"])
def parse_text_with_attachments() -> FlaskResponse:
    """Process multi-part form message with attachments.

    Converts attachments to tokens using docling, then
    calls the AI pipeline on the tokens + text and enqueue
    the entries in confirmation queue.

    Notes
    -----
    Requires multi-part form request due to attachments.
    Can be used with text only.

    Returns
    -------
    FlaskResponse
        Status.
    """
    username = request.form.get("username")
    if not username:
        return jsonify({"error": "No username provided"}), 400
    text = request.form.get("text")
    if not text:
        text = ""
    files: list[FileStorage] = request.files.getlist("files")
    if not files:
        files = []

    text = _append_attachments_to_text(files, text)
    entries = pipeline(text)
    for entry in entries:
        enqueue_confirmation(username, entry.model_dump_json())

    return (
        jsonify({"status": "processed"}),
        201,
    )


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "0") in ("1", "true", "True")
    app.run(
        debug=debug,
        host="0.0.0.0",
        port=int(os.environ.get("AI_SERVICE_PORT", 5300)),
        use_reloader=False,
    )
