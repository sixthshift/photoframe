# Raspberry Pi Photo Frame

This project turns your Raspberry Pi into a digital photo frame using a Waveshare 7.5-inch e-ink display. The photo frame renders webpages on your e-ink display with automatic updates.

## Hardware Requirements

- Raspberry Pi Zero W (or any Raspberry Pi model)
- Waveshare 7.5-inch e-ink display
- MicroSD card (8GB or larger recommended)
- Power supply for Raspberry Pi

## OS Installation

1. Download and install Raspberry Pi Imager on your computer.
2. Launch Raspberry Pi Imager and select "Choose OS".
3. In the "Operating System" section, select "Raspberry Pi OS (other)".
4. In the "Version" section, select "Raspberry Pi OS Lite (32-bit)".
5. In the "Settings" section (Advanced options)
	- Check "Set hostname" and set it to "photoframe"
	- Check "Enable SSH" and "use password authentication"
	- Check "Set username and password" and enter in a username and password (this will be your credentials to SSH into the raspberry pi)
	- Check "Configure wireless LAN" and enter in your WiFi SSID and password as well as setting "Wireless LAN country" to your country code
	- Check "Set locale settings" and choose your region/timezone
	- Click "Save"
6. Insert your MicroSD card into your computer and select it in the "Storage" section of Raspberry Pi Imager.
7. Click "Write" to flash the Raspberry Pi OS Lite image onto the SD card.
8. Once the flashing process is complete, insert the SD card into your Raspberry Pi.

## Installation

SSH into your Raspberry Pi and run the following command:

```bash
curl -sSL https://raw.githubusercontent.com/sixthshift/photoframe/main/install-remote.sh | bash
```

After installation completes, reboot your Raspberry Pi:

```bash
sudo reboot
```

## Basic Usage

The photo frame will automatically start on boot and display the default webpage. 

To change the URL or update interval, edit the run.sh file:

```bash
nano run.sh
```

Look for and modify these lines to customize your display:
```bash
DEFAULT_URL="https://example.com"
DEFAULT_INTERVAL=3600  # 1 hour in seconds (3600 = 1 hour)
```

## Configuring Your Photo Frame

To customize your photo frame display:

1. Edit the configuration file:
   ```bash
   nano config.ini
   ```

2. Modify the following settings:
   ```
   URL=https://your-website-here.com
   INTERVAL=3600
   ```

3. Save and exit (Ctrl+O, Enter, Ctrl+X)

4. Restart the photo frame:
   ```bash
   ./run.sh
   ```
   
   Or reboot:
   ```bash
   sudo reboot
   ```

## Technical Details

The photo frame uses:
- wkhtmltoimage for webpage rendering
- Pillow for image processing
- E-ink display optimizations for better battery life
- Configuration via config.ini

## License

MIT License
