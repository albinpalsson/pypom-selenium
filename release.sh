#!/bin/bash
set -euo pipefail
set -x

rm -rf dist || true
rm -rf venv || true
python3.14 -m venv venv
. venv/bin/activate
python -m pip install build==1.2.1 twine==6.2.0
python -m build
python -m twine upload dist/*