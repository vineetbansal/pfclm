#!/bin/bash
set -eo pipefail
IFS=$'\n\t'

/usr/bin/python3 -m virtualenv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
