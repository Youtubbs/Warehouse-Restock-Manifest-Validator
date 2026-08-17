import json
from pathlib import Path

from pydantic import ValidationError

from .exceptions import ManifestFormatError, ManifestNotFoundError
from .models import RestockItem

DEFAULT_MANIFEST_PATH = (
    Path(__file__).resolve().parents[1] / "data" / "restock_manifest.json"
)


# returns (valid items, error reports). each error report has index, row, errors
def load_manifest(
    path: str | Path = DEFAULT_MANIFEST_PATH,
) -> tuple[list[RestockItem], list[dict]]:
    path = Path(path)

    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError as e:
        raise ManifestNotFoundError(f"manifest not found: {path}") from e

    try:
        rows = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ManifestFormatError(f"manifest is not valid JSON: {path}") from e

    if not isinstance(rows, list):
        raise ManifestFormatError(
            f"manifest must be a list of rows, got {type(rows).__name__}"
        )

    items: list[RestockItem] = []
    errors: list[dict] = []

    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(
                {"index": index, "row": row, "errors": "row is not a JSON object"}
            )
            continue
        try:
            items.append(RestockItem.model_validate(row))
        except ValidationError as e:
            errors.append({"index": index, "row": row, "errors": e.errors()})

    return items, errors
