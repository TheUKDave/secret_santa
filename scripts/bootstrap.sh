#!/bin/bash
#
# Bootstrap virtualenv environment and postgres databases locally.
#
# NOTE: This script expects to be run from the project root with
# ./scripts/bootstrap.sh

set -o pipefail

# Install Python development dependencies
pip3 install -r requirements.txt

# Create Postgres databases
createdb santa

# Upgrade databases
source environment.sh
python manage.py migrate
