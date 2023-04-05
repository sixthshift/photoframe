from PIL import Image, ImageOps

def is_portrait(image):
    return image.width < image.height

class Photo:
    def __init__(self, path):
        self.path = path
        self.configure_orientation(False, False)

    def configure_orientation(self, flip_portrait, flip_landscape):
        self.portrait_orientation = 270 if flip_portrait else 90
        self.landscape_orientation = 180 if flip_landscape else 0
        return self

    def process(self):
        image = Image.open(self.path)
        if is_portrait(image):
            image = image.rotate(self.portrait_orientation)
        else:
            image = image.rotate(self.landscape_orientation)
        image = ImageOps.fit(image, (800,480), Image.ANTIALIAS)
        return image
