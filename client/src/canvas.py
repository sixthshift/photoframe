from PIL import Image, ImageOps

def is_portrait(image):
    return image.width < image.height

class Canvas:
    def __init__(self):
        self.configure_orientation(False, False)

    def configure_orientation(self, flip_portrait, flip_landscape):
        self.portrait_orientation = 270 if flip_portrait else 90
        self.landscape_orientation = 180 if flip_landscape else 0
        return self

    def draw(self, image_path):
        self.image = Image.open(image_path)
        return self

    def write(self, text):
        return self

    def process(self):
        if is_portrait(self.image):
            self.image = self.image.rotate(self.portrait_orientation)
        else:
            self.image = self.image.rotate(self.landscape_orientation)
        self.image = ImageOps.fit(self.image, (800,480), Image.ANTIALIAS)
        return self.image
