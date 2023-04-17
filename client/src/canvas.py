from io import BytesIO
import requests
from PIL import Image, ImageOps

def is_portrait(image):
    return image.width < image.height

class Canvas:
    def __init__(self):
        self.configure_alignment(False, False)

    def configure_alignment(self, flip_portrait, flip_landscape):
        self.portrait_alignment = 270 if flip_portrait else 90
        self.landscape_alignment = 180 if flip_landscape else 0
        return self

    def draw(self, url):
        response = requests.get(url)
        self.image = Image.open(BytesIO(response.content))
        return self

    def write(self, text):
        return self

    def process(self):
        if is_portrait(self.image):
            self.image = self.image.rotate(self.portrait_alignment)
        else:
            self.image = self.image.rotate(self.landscape_alignment)
        self.image = ImageOps.fit(self.image, (800,480), Image.ANTIALIAS)
        return self.image
