import argparse

from orientation import Orientation
from frame import Frame

parser = argparse.ArgumentParser("Photo Frame")

parser.add_argument('--image', type=str, required=True)
parser.add_argument('--orientation', type=str, choices=['landscape','portrait'], default='portrait')

args = parser.parse_args()

frame = Frame(Orientation[args.orientation])
frame.image(args.image)
frame.render()
frame.sleep()