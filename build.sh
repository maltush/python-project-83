#!/usr/bin/bash
set -e

curl -LsSf https://astral.sh/uv/install.sh | sh
source "$HOME/.local/bin/env"
make install

. .venv/bin/activate
pip install -e .