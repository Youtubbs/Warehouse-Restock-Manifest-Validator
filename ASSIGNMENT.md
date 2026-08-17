# Week 1 Assignment: Warehouse Restock Manifest Validator

## What this reinforces
This week's `support_api` project modeled tickets with Pydantic, gave them a
custom exception hierarchy, and defensively loaded a messy fixture — then
proved all of it with pytest. This assignment asks you to build that same
pattern (validated model → custom exceptions → skip-and-log loader → test
suite) from scratch, as a real Python project, against a different domain
and a different set of field constraints than the ones you typed this week.

## Objective
Build a Python project that validates a warehouse's restock manifest —
a batch of item rows that may contain some bad data — using a Pydantic v2
model, a custom exception hierarchy, and a defensive loader function, and
prove all of it works with a pytest test suite, structured as a proper
Python project (separate source and test files, not everything crammed
into one script) and pushed to its own GitHub repository.

When you're done, running `pytest` against your file should show every
test passing, including tests that confirm bad rows are skipped (not
crashed on) and that a missing manifest file raises your own exception
type, not a raw `FileNotFoundError`.

## Provided data
`restock_manifest.json` (in this same folder) is provided for you — **do
not edit its contents.** It's a 12-row manifest: 8 rows are valid, and 4
are deliberately broken, one per failure type this assignment tests for
(a `category` outside the allowed set, a negative `quantity`, a zero
`unit_cost`, and a row missing `sku` entirely). Your loader should be able
to run against it and report exactly 8 valid items and 4 errors.

Copy this file, unmodified, into your own repository (e.g. under a `data/`
folder) so your project is self-contained and runnable by anyone who
clones it — don't assume the grader has it sitting in a particular local
path. Reference it with a path relative to your own source file (e.g.
`Path(__file__).parent / "data" / "restock_manifest.json"`), not a
hardcoded absolute path.

## Requirements

**A Pydantic v2 model named `RestockItem`** with these fields:
- `sku: str`
- `warehouse: str`
- `quantity: int` — must be greater than 0 (reject zero and negative values)
- `unit_cost: float` — must be greater than 0
- `category: Literal["electronics", "perishable", "apparel", "hardware"]`

**A custom exception hierarchy** with at least:
- A base exception for anything this module can raise
- A specific subclass raised when the manifest file doesn't exist on disk
  (translate the standard library's `FileNotFoundError` into your own
  exception type, chained with `from` so the original error is still visible)

**A defensive loader function**, `load_manifest(path) -> tuple[list[RestockItem], list[dict]]`
(or an equivalent shape of your choosing — document it if you deviate),
that:
- Reads a JSON file containing a list of item rows (plain dicts)
- Validates each row into a `RestockItem`
- Skips any row that fails validation and collects it into an error report
  instead of letting the whole batch crash on one bad row
- Raises your custom "not found" exception (not a bare `FileNotFoundError`)
  if the file doesn't exist

**A pytest suite** (at least 5 tests, in its own test file — e.g. `tests/test_loader.py` — importing from your source module rather than duplicating logic) covering:
- A valid row loads correctly
- One `@pytest.mark.parametrize` test covering three invalid-field cases
  in a single test body — an out-of-set `category`, a non-positive
  `quantity`, and a non-positive `unit_cost` — each asserting
  `pytest.raises(ValidationError)`
- Loading the **provided** `restock_manifest.json` (see below) returns
  exactly 8 valid items and 4 errors — this is your proof that the loader
  handles a realistic, mixed-quality batch correctly
- A missing manifest path raises your custom exception, verified with
  `pytest.raises`

## Deliverable
A **public GitHub repository** containing your project. Submit the
repository URL on Canvas — nothing else.

Your repo must:
- Be organized as a real Python project, not one script: your `RestockItem`
  model, exception hierarchy, and `load_manifest` function live in a
  source file (or files) separate from your test file.
- Include the provided `restock_manifest.json`, unmodified, so the project
  runs standalone for anyone who clones it (see "Provided data" above).
- Include a `pyproject.toml` listing your
  dependencies (at minimum `pydantic` and `pytest`).
- Include a short `README.md` with the exact commands to set up a venv,
  install dependencies, and run the test suite.
- Include a `.gitignore` that excludes your virtual environment and
  `__pycache__` — don't commit either.
- Pass in full when a grader clones the repo fresh and runs `pytest` from
  the repo root.

## Time expectation
~1.5–2 hours, including repo setup — the GitHub/README overhead is a few
extra minutes, not a reason to scale up the coding requirements above.
