#!/bin/bash
set -e
DIR=$(dirname "$0")
TEMP_DIR=$(mktemp -d)
cp "$DIR"/../fetch_stock_data.py "$TEMP_DIR"/
cd "$TEMP_DIR"
pip install requests boto3 -t . >/dev/null
zip -r9 "$DIR/../lambda_function.zip" . >/dev/null
rm -rf "$TEMP_DIR"
