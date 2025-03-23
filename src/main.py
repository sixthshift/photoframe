#!/usr/bin/python
# -*- coding:utf-8 -*-
import argparse
import logging
import sys
import os
import hashlib
import time
import signal
from configparser import ConfigParser
from management import start_server

# Import directly from frame and webpage modules
from frame import Frame
from webpage import Webpage

logging.basicConfig(level=logging.DEBUG)

# Flag to handle graceful shutdown
running = True

def signal_handler(sig, frame):
    """Handle Ctrl+C for clean shutdown"""
    global running
    logging.info("Shutdown requested, exiting...")
    running = False

def render_once(url, renderer, frame):
    """Render a webpage once and exit"""
    try:
        logging.info(f"Rendering webpage: {url} in landscape orientation")
        image = renderer.capture(url)
        frame.render(image)
        frame.sleep()
        logging.info("Webpage rendered successfully")
    except Exception as e:
        logging.error(f"Error: {e}")
    finally:
        logging.info("Finished rendering webpage")

def auto_update(url, interval, renderer, frame):
    """Automatically update the display at regular intervals"""
    global running
    logging.info(f"Auto-update mode: refreshing every {interval} seconds. Press Ctrl+C to exit.")
    
    try:
        while running:
            try:
                # Render the webpage
                logging.info(f"Rendering webpage: {url}")
                image = renderer.capture(url)
                frame.render(image)
                
                # Exit if shutdown requested
                if not running:
                    break
                    
                # Wait for next update
                wait_for_next_update(interval)
                    
            except Exception as e:
                logging.error(f"Error during update: {e}")
                # Wait before retry on error
                time.sleep(min(interval, 10))
                
    finally:
        # Clean shutdown
        logging.info("Shutting down...")
        frame.sleep()
        logging.info("E-ink display put to sleep")

def wait_for_next_update(interval):
    """Wait for the next update while checking for shutdown requests"""
    global running
    logging.info(f"Waiting {interval} seconds until next update...")
    
    # Break the sleep into smaller chunks to check running flag
    remaining = interval
    while remaining > 0 and running:
        chunk = min(remaining, 1)  # Sleep at most 1 second at a time
        time.sleep(chunk)
        remaining -= chunk

def refresh_display():
    """Function to refresh the display on demand"""
    global renderer, frame, url
    try:
        logging.info(f"Manual refresh triggered for URL: {url}")
        image = renderer.capture(url)
        frame.render(image)
        logging.info("Manual refresh complete")
    except Exception as e:
        logging.error(f"Error during manual refresh: {e}")

def main():
    global url, renderer, frame
    
    # Read from config file first
    config_parser = ConfigParser()
    if os.path.exists('config.ini'):
        config_parser.read('config.ini')
        url = config_parser.get('DEFAULT', 'URL', fallback=None)
        interval = config_parser.getint('DEFAULT', 'INTERVAL', fallback=3600)
    else:
        url = None
        interval = 3600
    
    # Command line arguments override config file
    parser = argparse.ArgumentParser(description='Render webpage on e-ink display')
    parser.add_argument('--url', type=str, help='URL of image to render')
    parser.add_argument('--interval', type=int, default=interval, help='Update interval in seconds (0 = run once)')
    parser.add_argument('--port', type=int, default=80, help='Port for management server')
    args = parser.parse_args()
    
    # Command line args take precedence
    if args.url:
        url = args.url
    
    # If no URL provided in config or command line, exit
    if not url:
        logging.error("No URL provided. Please specify in config.ini or with --url")
        sys.exit(1)
    
    # Register signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    # Create renderer and frame
    renderer = Webpage(width=Frame.WIDTH, height=Frame.HEIGHT)
    frame = Frame()
    
    # Start management server
    start_server(refresh_callback=refresh_display, port=args.port)
    
    # Run once or continuously based on interval
    if args.interval <= 0:
        render_once(url, renderer, frame)
    else:
        auto_update(url, args.interval, renderer, frame)

if __name__ == '__main__':
    main() 