#!/bin/bash

# Install nodejs
if ! command -v node &> /dev/null; then
    echo "Node.js is not installed. Installing Node.js..."
    if [ "$(uname -m)" != "armv6l" ]; then
        curl -sL https://deb.nodesource.com/setup_16.x | bash -
    else
        wget -O - https://raw.githubusercontent.com/sdesalas/node-pi-zero/master/install-node-v16.3.0.sh | bash
    fi
    apt-get -y install nodejs
fi

if ! command -v npm &> /dev/null; then
    echo "npm is not installed. Installing npm..."
    npm install -g npm@8.19.4
fi


