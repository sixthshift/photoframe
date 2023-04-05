import os
from lib.waveshare_epd import epd7in5_V2
from photo import Photo

picdir = picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
class Frame:
    def __init__(self):
        self.epd = epd7in5_V2.EPD()
        self.epd.init()
    
    def draw(self, image):
        photo = (
            Photo(os.path.join(picdir, image))
            .configure_orientation(True, True)
            .process()
        )
        self.epd.display(self.epd.getbuffer(photo))
        return self

    def message(self, text):
        pass

    def clear(self):
        self.epd.Clear()

    def sleep(self):
        self.epd.sleep()