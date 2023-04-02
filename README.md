# Raspberry Pi Photo Frame

This project turns your Raspberry Pi into a photo frame using a Waveshare 7-inch e-ink display. The Python script displays photos from a specified directory and allows you to navigate through them using two push buttons.

## Hardware
- Raspberry Pi Zero W
- Waveshare 7-inch e-ink display
- MicroSD card

## OS Installation
1. Download and install Raspberry Pi Imager on your computer.
2. Launch Raspberry Pi Imager and select "Choose OS".
3. In the "Operating System" section, select "Raspberry Pi OS (other)".
4. In the "Version" section, select "Raspberry Pi OS Lite (32-bit)".
5. In the "Settings" section (Advanced options)
	- Check "Enable SSH" and "use password authentication"
	- Check "Set username and password" and enter in a username and password (this will be your credentials to SSH into the raspberry pi)
	- Check "Configure wireless LAN" and enter in your WiFi SSID and password as well as setting "Wireless LAN country" to AU
	- Check "Set locale settings" and choose Austraila/Sydney
	- Click "Save"
6. Insert your MicroSD card into your computer and select it in the "Storage" section of Raspberry Pi Imager.
7. Click "Write" to flash the Raspberry Pi OS Lite image onto the SD card.
8. Once the flashing process is complete, insert the SD card into your Raspberry Pi.

## OS Configuration
1. Run the following commands to update the Raspberry Pi OS and install necessary packages:
	```bash
	sudo apt-get update
	sudo apt-get upgrade
	sudo apt-get install python3-pip libopenjp2-7 libtiff5
	sudo pip3 install Pillow
	```
2. Edit the /etc/hostname file and replace raspberrypi with photoframe. This will change the hostname of your Raspberry Pi to photoframe, which is required for the Python script to access the e-ink display.

3. Edit the /etc/hosts file and add the following line at the end of the file. This will associate the hostname photoframe with the loopback IP address.
	```
	127.0.1.1   photoframe
	```
4. Clone this repository onto your Raspberry Pi
	```
	git clone git@github.com:sixthshift/photo-frame.git
	```
5. Open `/etc/rc.local` and add the following before the `exit 0` line
	```
	/usr/bin/python3 /home/admin/photo-frame/photo_frame.py &
	```
6. Reboot the Raspberry Pi, the photo frame software automatically upon boot.
	```
	sudo reboot
	```