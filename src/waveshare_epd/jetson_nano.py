# JetsonNano e-Paper Display Driver Implementation
# Extracted from epdconfig.py for platform-specific implementation

import os
import time
import logging
import ctypes

logger = logging.getLogger(__name__)

class JetsonNano:
    # Pin definition
    RST_PIN = 17
    DC_PIN = 25
    CS_PIN = 8
    BUSY_PIN = 24

    def __init__(self):
        find_dirs = [
            os.path.dirname(os.path.realpath(__file__)),
            "/usr/local/lib",
            "/usr/lib",
        ]
        self.SPI = None
        for find_dir in find_dirs:
            so_filename = os.path.join(find_dir, "sysfs_software_spi.so")
            if os.path.exists(so_filename):
                self.SPI = ctypes.cdll.LoadLibrary(so_filename)
                break
        if self.SPI is None:
            raise RuntimeError("Cannot find sysfs_software_spi.so")

        import Jetson.GPIO
        self.GPIO = Jetson.GPIO

    def digital_write(self, pin, value):
        self.GPIO.output(pin, value)

    def digital_read(self, pin):
        return self.GPIO.input(self.BUSY_PIN)

    def delay_ms(self, delaytime):
        time.sleep(delaytime / 1000.0)

    def spi_writebyte(self, data):
        self.SPI.SYSFS_software_spi_transfer(data[0])

    def module_init(self):
        self.GPIO.setmode(self.GPIO.BCM)
        self.GPIO.setwarnings(False)
        self.GPIO.setup(self.RST_PIN, self.GPIO.OUT)
        self.GPIO.setup(self.DC_PIN, self.GPIO.OUT)
        self.GPIO.setup(self.CS_PIN, self.GPIO.OUT)
        self.GPIO.setup(self.BUSY_PIN, self.GPIO.IN)
        self.SPI.SYSFS_software_spi_begin()
        return 0

    def module_exit(self):
        logger.debug("spi end")
        self.SPI.SYSFS_software_spi_end()

        logger.debug("close 5V, Module enters 0 power consumption ...")
        self.GPIO.output(self.RST_PIN, 0)
        self.GPIO.output(self.DC_PIN, 0)

        self.GPIO.cleanup([self.RST_PIN, self.DC_PIN, self.CS_PIN, self.BUSY_PIN]) 