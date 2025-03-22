#!/bin/bash

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Activate virtual environment if it exists
if [ -d "$SCRIPT_DIR/venv" ]; then
    source "$SCRIPT_DIR/venv/bin/activate"
fi

# Default settings
DEFAULT_URL="https://example.com"
DEFAULT_INTERVAL=3600  # 1 hour in seconds

# Load config file if it exists
CONFIG_FILE="$SCRIPT_DIR/config.ini"
if [ -f "$CONFIG_FILE" ]; then
    echo "Loading configuration from config.ini"
    
    # Read URL from config file
    CONFIG_URL=$(grep -E "^URL=" "$CONFIG_FILE" | cut -d= -f2)
    if [ ! -z "$CONFIG_URL" ]; then
        URL="$CONFIG_URL"
    else
        URL="$DEFAULT_URL"
    fi
    
    # Read interval from config file
    CONFIG_INTERVAL=$(grep -E "^INTERVAL=" "$CONFIG_FILE" | cut -d= -f2)
    if [ ! -z "$CONFIG_INTERVAL" ]; then
        INTERVAL="$CONFIG_INTERVAL"
    else
        INTERVAL="$DEFAULT_INTERVAL"
    fi
else
    echo "No config.ini found. Using defaults."
    URL="$DEFAULT_URL"
    INTERVAL="$DEFAULT_INTERVAL"
fi

echo "Starting photo frame with URL: $URL and interval: $INTERVAL seconds"

# Run the main Python script with parameters
python "$SCRIPT_DIR/src/main.py" --url "$URL" --interval "$INTERVAL" 