from luma.core.interface.serial import spi, noop
from luma.led_matrix.device import max7219
from PIL import Image


serial = spi(port=0, device=0, gpio=noop(), block_orientation=-90)
device = max7219(serial, width=8, height=32, rotate=1)


def display_image(image_path):
    img = Image.open(image_path).convert("1")
    device.display(img)

def clear_display():
    device.clear()

