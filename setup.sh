#!/bin/bash
set -eo pipefail
IFS=$'\n\t'

python3 -m virtualenv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
