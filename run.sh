#!/bin/bash

# Check if the required arguments are passed
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 -fp <filepath> -e <extension>"
    exit 1
fi

# Execute the Docker command with passed arguments
docker run -it \
  -v $(pwd)/output:/app/output/ \
  --mount type=bind,source="$(pwd)/$2",target=/app/$2,readonly \
  proto_compiler python3 cli.py "$@"
