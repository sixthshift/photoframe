import os
import logging
import tempfile
import subprocess
from PIL import Image

class Webpage:
    def __init__(self, width=800, height=480):
        """Initialize the webpage renderer with specified dimensions"""
        self.width = width
        self.height = height
        logging.info(f"Initialized webpage renderer with dimensions: {width}x{height}")

    def capture(self, url):
        """Download image directly using curl and process with PIL"""
        logging.info(f"Downloading image from: {url}")
        
        # Create a temporary file for the image
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp:
            temp_filename = temp.name
        
        try:
            # Download the image directly using curl
            subprocess.run(['curl', '-s', '-o', temp_filename, url], check=True, timeout=30)
            
            # Open the downloaded image
            image = Image.open(temp_filename)
            
            # Resize image if needed, preserving aspect ratio
            if image.width != self.width or image.height != self.height:
                # Calculate the resize ratio to fit within the display dimensions
                # while preserving aspect ratio
                ratio_w = self.width / image.width
                ratio_h = self.height / image.height
                ratio = min(ratio_w, ratio_h)  # Use the smaller ratio to fit within bounds
                
                # Calculate new dimensions
                new_width = int(image.width * ratio)
                new_height = int(image.height * ratio)
                
                logging.info(f"Resizing from {image.width}x{image.height} to {new_width}x{new_height} (preserving aspect ratio)")
                image = image.resize((new_width, new_height), Image.LANCZOS)
                
                # Create a blank white canvas of the target size
                canvas = Image.new('RGB', (self.width, self.height), (255, 255, 255))
                
                # Calculate position to center the image on the canvas
                x_offset = (self.width - new_width) // 2
                y_offset = (self.height - new_height) // 2
                
                # Paste the resized image onto the canvas
                canvas.paste(image, (x_offset, y_offset))
                
                # Use the canvas as our image
                image = canvas
            
            # Convert to black and white for e-ink display
            image = image.convert('1')
            
            logging.info(f"Successfully processed image, size: {image.size}")
            
            return image
            
        except Exception as e:
            logging.error(f"Error downloading/processing image: {e}")
            # Create a blank image
            return Image.new('1', (self.width, self.height), 255)
            
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_filename):
                os.remove(temp_filename) 