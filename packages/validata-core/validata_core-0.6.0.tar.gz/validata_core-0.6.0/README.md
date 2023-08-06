# Validata validation core

[![PyPI](https://img.shields.io/pypi/v/validata-core.svg)](https://pypi.python.org/pypi/validata-core)

Validata validation library built over [frictionless-py](https://github.com/frictionlessdata/frictionless-py) `3.*`. Validata core provides french error messages.

## Try

Create a virtualenv, run the script against fixtures:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
validata --schema /path/to/schema.json table.csv
```

## Testing

```bash
pip install pytest
pytest --doctest-modules
```
