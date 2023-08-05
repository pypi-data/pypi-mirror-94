import logging

import numpy as np
import skimage.draw
from PIL import Image as pilImage, ImageDraw, ImageFont

from dtoolbioimage import scale_to_uint8
from dtoolbioimage import Image as dbiImage


logger = logging.getLogger(__name__)


class AnnotatedImage(object):

    @classmethod
    def from_image(cls, im):
        self = cls()
        self.im = im.view(dbiImage)
        self.canvas = np.zeros_like(im)

        logger.info(f"Created canvas with shape {self.canvas.shape}")

        return self

    def _repr_png_(self):
        return self.canvas.view(dbiImage)._repr_png_()

    def mark_mask(self, mask, col=(255, 255, 255)):
        self.canvas[np.where(mask)] = col

    def draw_line_aa(self, p0, p1, col):

        # print(f"{self.canvas.shape}, draw {p0} to {p1}")

        r0, c0 = p0
        r1, c1 = p1
        rr, cc, aa = skimage.draw.line_aa(r0, c0, r1, c1)

        try:
            self.canvas[rr, cc] = col
        except IndexError:
            pass

    def draw_disk(self, p, radius, col):
        rr, cc = skimage.draw.disk(p, radius)
        self.canvas[rr, cc] = col

    @property
    def merged_im(self):
        return 0.5 * self.im + 0.5 * self.canvas

    def save(self, filename):
        self.merged_im.view(dbiImage).save(filename)

    def text_at(self, p, text, size=36, color=(255, 255, 255)):
        pilim = pilImage.fromarray(self.canvas)
        draw = ImageDraw.ImageDraw(pilim)
        fnt = ImageFont.truetype('Microsoft Sans Serif.ttf', size=size)
        draw.text(p, text, font=fnt, fill=color)

        self.canvas = np.array(pilim)
