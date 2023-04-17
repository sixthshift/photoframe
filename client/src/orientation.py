from enum import Enum

class Orientation(Enum):
    landscape = False
    portrait = True

    def __str__(self):
        return self.name