#!/bin/bash
set -euo pipefail
set -x

rm -rf dist || true
rm -rf venv || true
python3.12 -m venv venv
. venv/bin/activate
python -m pip install build==1.2.1 twine==5.1.1
python -m build
python -m twine upload dist/*