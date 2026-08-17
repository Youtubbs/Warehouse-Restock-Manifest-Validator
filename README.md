# Warehouse Restock Manifest Validator

Validates a warehouse restock manifest with a Pydantic v2 model. See ASSIGNMENT.md to see specifics. See pyproject.toml for python requirements.

## Setup

```bash
git clone <this-repo-url>
cd project
python -m venv .venv
source .venv/bin/activate OR .\.venv\Scripts\activate.bat
pip install -e ".[test]"
```

## Run the tests

```bash
pytest -q
```

If pytest isn't working, it's probably the wrong interpreter! Try python -m pytest -q instead if this is the case to force usage of local venv.

## Run the validator

```bash
python main.py
```

Pass a path to validate a different file from default. e.g. `python main.py path/to/manifest.json`.