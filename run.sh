#!/bin/bash

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Ensure we have proper permissions for the script directory
if [ ! -w "$SCRIPT_DIR" ]; then
    echo "Error: Cannot write to script directory: $SCRIPT_DIR"
    exit 1
fi

# Define the virtual environment location
VENV_DIR="$SCRIPT_DIR/venv"

# Make sure dependencies for virtual environment are installed
setup_system_dependencies() {
    echo "Checking system dependencies..."
    
    # Check if pip and venv are installed
    if ! command -v python3 &> /dev/null || ! python3 -c "import venv" &> /dev/null; then
        echo "Installing Python dependencies..."
        sudo apt-get update
        sudo apt-get install -y python3-pip python3-venv libopenjp2-7 python3-pil
    fi
}

# Check if virtual environment exists, create it if it doesn't
if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment not found. Creating one at $VENV_DIR..."
    
    # Ensure system dependencies
    setup_system_dependencies
    
    # Create virtual environment
    python3 -m venv "$VENV_DIR"
    
    # Check if venv was created successfully
    if [ ! -d "$VENV_DIR" ]; then
        echo "Error: Failed to create virtual environment."
        echo "Falling back to system Python..."
    else
        echo "Virtual environment created at $VENV_DIR"
        
        # Activate the new virtual environment
        source "$VENV_DIR/bin/activate"
        
        # Install required packages
        echo "Installing required packages..."
        pip install --upgrade pip
        if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
            pip install -r "$SCRIPT_DIR/requirements.txt"
        else
            echo "Warning: requirements.txt not found. Installing minimal requirements..."
            pip install pillow
        fi
        
        echo "Virtual environment created and dependencies installed."
    fi
else
    # Activate existing virtual environment
    echo "Activating virtual environment at $VENV_DIR"
    source "$VENV_DIR/bin/activate" || {
        echo "Error: Failed to activate virtual environment."
        echo "Attempting to recreate virtual environment..."
        
        # Remove corrupted venv
        rm -rf "$VENV_DIR"
        
        # Retry setup by running the script again
        exec "$0" "$@"
        exit $?
    }
    
    echo "Successfully activated virtual environment"
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
if [ -d "$VENV_DIR" ] && [ -f "$VENV_DIR/bin/python" ]; then
    # Use the Python from the virtual environment directly
    "$VENV_DIR/bin/python" "$SCRIPT_DIR/src/main.py" --url "$URL" --interval "$INTERVAL"
else
    # Fallback to system Python
    echo "Warning: Using system Python as fallback"
    python3 "$SCRIPT_DIR/src/main.py" --url "$URL" --interval "$INTERVAL" 
fi