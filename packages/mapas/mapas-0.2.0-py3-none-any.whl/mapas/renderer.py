from io import BytesIO
from typing import Tuple

from PIL import Image


class Renderer:
    ''' Manages the render into an image, used to abstract the library used for
    drawing, so it can be easily replaced, upgraded or fixed '''

    def __init__(self, width, height):
        self.image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        self.width = width
        self.height = height

    def paste(self, image: bytes, box: Tuple[int, int] = (0, 0)):
        img = Image.open(BytesIO(image))

        self.image.paste(img, box=box)

    def alpha_composite(self, image: bytes):
        img = Image.open(BytesIO(image))
        self.image = Image.alpha_composite(self.image, img)

    def getpixel(self, pixel: Tuple[int, int]) -> Tuple[int, int, int, int]:
        return self.image.getpixel(pixel)

    def get_png_bytes(self) -> BytesIO:
        fp = BytesIO()
        self.image.save(fp, format='png')

        return fp

    def save(self, filename: str):
        self.image.save(filename)
