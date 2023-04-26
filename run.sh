#!/bin/bash

# Check if running as root
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi
cd server/src
# Start the server
sudo node ./server /home/admin/photos/