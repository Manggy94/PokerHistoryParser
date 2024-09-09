#!/bin/sh
pwd
# Build the function layer
pip install -r requirements.txt -t tmp/layer

# Zip the function layer
python3 scripts/zip_to_lambda.py

# Delete the temporary directory
rm -rf tmp