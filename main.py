import sys

from restock import DEFAULT_MANIFEST_PATH, ManifestError, load_manifest


def main() -> int:
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_MANIFEST_PATH

    try:
        items, errors = load_manifest(path)
    except ManifestError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    print(f"{len(items)} valid items, {len(errors)} errors")

    for item in items:
        print(
            f"  {item.sku:<10} {item.warehouse:<8} {item.category:<12} {item.line_total:>10.2f}"
        )

    for error in errors:
        row, details = error["row"], error["errors"]
        sku = row.get("sku", "<missing sku>") if isinstance(row, dict) else "?"
        fields = (
            ", ".join(str(d["loc"][0]) for d in details)
            if isinstance(details, list)
            else details
        )
        print(f"  row {error['index']}: {sku} rejected ({fields})", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
