#!/bin/bash

# Exit on any error
set -e

echo "========================================"
echo "Photo Frame - Automated Setup Script"
echo "========================================"

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "[1/6] Updating system packages..."
sudo apt update
sudo apt upgrade -y
sudo apt install -y git python3-pip python3-venv python3-full

# Add Pillow system dependencies (simpler for older Pillow version)
echo "Installing Pillow dependencies..."
sudo apt install -y libopenjp2-7

echo "[2/6] Creating Python virtual environment..."
# Create virtual environment
python3 -m venv "$SCRIPT_DIR/venv"
# Activate the virtual environment
source "$SCRIPT_DIR/venv/bin/activate"

echo "[3/6] Creating Python environment and installing dependencies..."
# Increase swap to avoid memory issues during installation
echo "Temporarily increasing swap space for installation..."
sudo sed -i 's/CONF_SWAPSIZE=100/CONF_SWAPSIZE=1024/' /etc/dphys-swapfile
sudo /etc/init.d/dphys-swapfile restart

# Install Python packages with optimized settings
echo "Installing Python requirements (this may take a while)..."
pip install --upgrade pip
pip install -r requirements.txt --timeout 300 --no-cache-dir

# Reset swap configuration
echo "Resetting swap space..."
sudo sed -i 's/CONF_SWAPSIZE=1024/CONF_SWAPSIZE=100/' /etc/dphys-swapfile
sudo /etc/init.d/dphys-swapfile restart

echo "[4/6] Enabling SPI interface..."
# Enable SPI without user interaction
if ! grep -q "dtparam=spi=on" /boot/config.txt; then
    echo "dtparam=spi=on" | sudo tee -a /boot/config.txt
    echo "SPI interface enabled."
else
    echo "SPI interface was already enabled."
fi


echo "[5/6] Setting permissions..."
# Make scripts executable
chmod +x run.sh

echo "[6/6] Setting up systemd service for autostart..."
# Create a systemd service file
SERVICE_NAME="photoframe"
SERVICE_PATH="/etc/systemd/system/${SERVICE_NAME}.service"

# Get current username
USERNAME=$(whoami)
echo "Setting up service to run as user: $USERNAME"

# Copy the service file to systemd directory with proper substitutions
echo "Creating systemd service file: $SERVICE_PATH"
cp photoframe.service /tmp/photoframe.service.tmp
sed -i "s|%USER%|${USERNAME}|g" /tmp/photoframe.service.tmp
sed -i "s|%WORKDIR%|${SCRIPT_DIR}|g" /tmp/photoframe.service.tmp
sudo mv /tmp/photoframe.service.tmp "${SERVICE_PATH}"

# Reload systemd to recognize the new service
echo "Enabling and starting the service..."
sudo systemctl daemon-reload
sudo systemctl enable ${SERVICE_NAME}.service
sudo systemctl restart ${SERVICE_NAME}.service

echo "Service status:"
sudo systemctl status ${SERVICE_NAME}.service --no-pager

# Create logs directory
mkdir -p logs

echo "========================================"
echo "Setup completed successfully!"
echo "Please reboot your Raspberry Pi to start the photo frame."
echo "Run: sudo reboot"
echo "========================================" 