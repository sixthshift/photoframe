#!/bin/bash

echo "====================================================="
echo "Raspberry Pi Photo Frame - Remote Installation Script"
echo "====================================================="

# Check for git
if ! [ -x "$(command -v git)" ]; then
  echo "Installing git..."
  sudo apt update
  sudo apt install -y git
fi

# Clone the repository
echo "Cloning the photoframe repository..."
git clone https://github.com/sixthshift/photoframe.git
cd photoframe

# Run the setup script
echo "Running setup script..."
chmod +x setup.sh
./setup.sh

echo "====================================================="
echo "Installation complete! Please reboot your Raspberry Pi."
echo "Run: sudo reboot"
echo "=====================================================" 