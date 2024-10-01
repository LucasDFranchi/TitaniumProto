#!/bin/bash

# Check if the required arguments are passed
if [ "$#" -lt 4 ]; then
    echo "Usage: $0 -fp <filepath> -e <extension>"
    exit 1
fi

# Initialize variables
filepath=""
extension=""

# Parse arguments
while [ "$#" -gt 0 ]; do
    case $1 in
        -fp) filepath="$2"; shift ;;
        -e) extension="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# Validate filepath
if [ ! -f "$filepath" ]; then
    echo "File not found: $filepath"
    exit 1
fi

# Execute the Docker command with the validated arguments
docker run -it \
  -v "$(pwd)/output:/app/output/" \
  -v "$(pwd)/$filepath:/app/$filepath" \
  proto_compiler python3 cli.py -fp "$filepath" -e "$extension"
