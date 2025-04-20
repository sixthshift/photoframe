from PIL import Image
import hashlib
from waveshare_epd import epd7in5_V2
import logging

class Frame:
    # Class properties for dimensions
    WIDTH = 800
    HEIGHT = 480
    
    def __init__(self):
        self.epd = epd7in5_V2.EPD()
        self.epd.init()
        self.last_image_hash = None
        
        # Render a blank image
        self.clear()
        
    def _hash_image(self, image):
        """Generate a hash for the image to detect changes"""
        # Convert PIL image to bytes directly and hash it
        return hashlib.md5(image.tobytes()).hexdigest()

    def clear(self):
        self.write_to_display(Image.new('1', (self.WIDTH, self.HEIGHT), 255))
        
    def render(self, image):
        # Calculate hash of the new image
        hash = self._hash_image(image)
        
        # Only render if the image has changed
        if hash != self.last_image_hash:
            logging.info("Image changed, rendering to e-ink display")
            self.clear()
            self.write_to_display(image)
            # Update the last image hash
            self.last_image_hash = hash
        else:
            logging.info("Image unchanged, skipping rendering")

    def write_to_display(self, image):
        # Convert the provided image for the e-ink display
        buffer = self.epd.getbuffer(image)
        # Display on the e-ink screen
        self.epd.display(buffer)
        
    def sleep(self):
        # Put the display into sleep mode to conserve power
        self.epd.sleep() 