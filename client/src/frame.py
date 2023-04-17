import os
from lib.waveshare_epd import epd7in5_V2
from canvas import Canvas

class Frame:
    def __init__(self, orientation):
        self.epd = epd7in5_V2.EPD()
        self.epd.init()
        self.canvas = Canvas().configure_alignment(True, False)
        self.orientation = orientation

    def image(self, url):
        self.canvas.draw(url)
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
