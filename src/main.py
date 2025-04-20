#!/usr/bin/python
# -*- coding:utf-8 -*-
import argparse
import logging
import sys
import os
import hashlib
import time
import signal
import traceback

# Import directly from frame and webpage modules
from frame import Frame
from webpage import Webpage

# Set up logging to file as well as console
log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "photoframe.log")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

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
        logging.error(traceback.format_exc())
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

def main():
    try:
        parser = argparse.ArgumentParser(description='Render webpage on e-ink display')
        parser.add_argument('--url', type=str, required=True, help='URL of webpage to render')
        parser.add_argument('--interval', type=int, default=0, help='Update interval in seconds (0 = run once)')
        args = parser.parse_args()

        # Log startup information
        logging.info(f"Starting photoframe application")
        logging.info(f"Python version: {sys.version}")
        logging.info(f"URL: {args.url}")
        logging.info(f"Interval: {args.interval} seconds")
        
        # Register signal handler for Ctrl+C
        signal.signal(signal.SIGINT, signal_handler)
        
        # Create renderer and frame
        logging.info("Initializing web renderer...")
        renderer = Webpage()
        
        logging.info("Initializing e-ink frame...")
        try:
            frame = Frame()
        except Exception as e:
            logging.error(f"Failed to initialize e-ink display: {e}")
            logging.error(traceback.format_exc())
            logging.error("Check if SPI is enabled and the display is properly connected")
            sys.exit(1)
        
        # Run once or continuously based on interval
        if args.interval <= 0:
            render_once(args.url, renderer, frame)
        else:
            auto_update(args.url, args.interval, renderer, frame)
            
    except Exception as e:
        logging.error(f"Unhandled exception in main: {e}")
        logging.error(traceback.format_exc())
        sys.exit(1)

if __name__ == '__main__':
    main() 