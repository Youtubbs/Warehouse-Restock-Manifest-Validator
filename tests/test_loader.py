import json

import pytest
from pydantic import ValidationError

from restock import (
    DEFAULT_MANIFEST_PATH,
    ManifestError,
    ManifestFormatError,
    ManifestNotFoundError,
    RestockItem,
    load_manifest,
)

VALID_ROW = {
    "sku": "SKU-2001",
    "warehouse": "west-1",
    "quantity": 12,
    "unit_cost": 7.25,
    "category": "hardware",
}


def test_valid_row_loads():
    item = RestockItem.model_validate(VALID_ROW)

    assert item.sku == "SKU-2001"
    assert item.quantity == 12
    assert item.category == "hardware"


@pytest.mark.parametrize(
    "field, bad_value",
    [
        ("category", "furniture"),
        ("quantity", -5),
        ("unit_cost", 0),
    ],
)
def test_invalid_field_rejected(field, bad_value):
    row = VALID_ROW | {field: bad_value}

    with pytest.raises(ValidationError):
        RestockItem.model_validate(row)


def test_provided_manifest_splits_valid_and_invalid():
    items, errors = load_manifest(DEFAULT_MANIFEST_PATH)

    assert len(items) == 8
    assert len(errors) == 4


def test_missing_manifest_raises_custom_exception(tmp_path):
    missing = tmp_path / "nope.json"

    with pytest.raises(ManifestNotFoundError) as e:
        load_manifest(missing)

    assert isinstance(e.value, ManifestError)
    assert isinstance(e.value.__cause__, FileNotFoundError)


def test_malformed_json_raises_format_error(tmp_path):
    broken = tmp_path / "broken.json"
    broken.write_text("{not json", encoding="utf-8")

    with pytest.raises(ManifestFormatError):
        load_manifest(broken)


def test_error_report_keeps_original_rows(tmp_path):
    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        json.dumps([VALID_ROW, {"warehouse": "west-1"}]), encoding="utf-8"
    )

    items, errors = load_manifest(manifest)

    assert [item.sku for item in items] == ["SKU-2001"]
    assert errors[0]["row"] == {"warehouse": "west-1"}
