from contextlib import contextmanager
import os
import tempfile


from docling.datamodel.accelerator_options import AcceleratorDevice, AcceleratorOptions
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from werkzeug.datastructures import FileStorage


from collections.abc import Sequence
from pathlib import Path

accelerator_options = AcceleratorOptions(num_threads=8, device=AcceleratorDevice.CPU)

pipeline_options = PdfPipelineOptions()
pipeline_options.accelerator_options = accelerator_options

# TODO: Do you need to specify cpu for each input type?
converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(
            pipeline_options=pipeline_options,
        ),
    }
)


def _convert_attachments_to_text(files: Sequence[FileStorage | str | Path]) -> str:
    parts = []
    for i, f in enumerate(files):
        with _as_path(f) as p:
            result = converter.convert(p)
            parts.append(f"ATTACHMENT {i}: \n{result.document.export_to_markdown()}")
    return "\n".join(parts) + ("\n" if parts else "")


def append_attachments_to_text(
    files: Sequence[FileStorage | str | Path], text: str
) -> str:
    """Converts and appends attachments as strings to text.

    Uses docling to process attachments

    Parameters
    ----------
    files : Sequence[FileStorage  |  str  |  Path]
        Sequence of files in various forms.
    text : str
        Text to append to. Can be empty.

    Returns
    -------
    str
        Input text with appended attachment strings.
    """
    text += "\n\nAttachments: \n------------------\n\n"
    text += _convert_attachments_to_text(files)
    return text


@contextmanager
def _as_path(f: FileStorage | str | Path):
    if isinstance(f, (str, Path)):
        yield str(f)
    else:
        ext = Path(f.filename or "").suffix
        with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
            f.save(tmp.name)
            tmp_path = tmp.name
        try:
            yield tmp_path
        finally:
            os.remove(tmp_path)
