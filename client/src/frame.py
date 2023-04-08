import os
from lib.waveshare_epd import epd7in5_V2
from canvas import Canvas

picdir = picdir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))), 'pic')


class Frame:
    def __init__(self):
        self.epd = epd7in5_V2.EPD()
        self.epd.init()
        self.canvas = Canvas().configure_orientation(True, False)

    def image(self, image):
        self.canvas.draw(os.path.join(picdir, image))
        return self

    def message(self, text):
        return self

    def render(self):

        self.epd.display(self.epd.getbuffer(self.canvas.process()))
        return self

    def clear(self):
        self.epd.Clear()
        return self

    def sleep(self):
        self.epd.sleep()
        return self

    def destroy(self):
        self.epd
