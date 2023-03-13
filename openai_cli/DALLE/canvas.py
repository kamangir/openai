from io import BytesIO
from PIL import Image
from enum import Enum
import requests
import numpy as np
from openai_cli import NAME, VERSION
from abcli.modules.objects import signature as object_signature
from abcli.modules.host import signature as host_signature
from abcli.modules.host import is_jupyter
from abcli.plugins.graphics import add_signature
from abcli import file
import abcli.logging
import logging


logger = logging.getLogger()


class Canvas(object):
    def __init__(
        self,
        width=4096,
        height=2048,
        verbose=False,
        debug_mode=False,
        dryrun=False,
    ):
        self.verbose = verbose
        self.debug_mode = debug_mode
        self.dryrun = dryrun
        self.is_jupyter = is_jupyter()

        self.width = width
        self.height = height

        self.image = Image.new(
            "RGB",
            (self.width, self.height),
            (0, 0, 0),
        )
        self.mask = Image.new(
            "L",
            (self.width, self.height),
            (0,),
        )

    def box(self):
        indices = np.nonzero(np.array(self.mask) == 255)

        left = indices[1].min()
        top = indices[0].min()
        right = indices[1].max()
        bottom = indices[0].max()

        return (left, top, right, bottom)

    def generate(self, brush, prompt):
        import openai

        box = (
            brush.cursor[0] - brush.width // 2,  # left,
            brush.cursor[1] - brush.height // 2,  # top,
            brush.cursor[0] + brush.width // 2,  # right,
            brush.cursor[1] + brush.height // 2,  # bottom,
        )

        image_ = self.image.crop(box)
        image_byte_stream = BytesIO()
        image_.save(image_byte_stream, format="PNG")
        image_byte_array = image_byte_stream.getvalue()

        mask_ = image_.copy().convert("RGBA")
        mask_.putalpha(self.mask.crop(box))
        mask_byte_stream = BytesIO()
        mask_.save(mask_byte_stream, format="PNG")
        mask_byte_array = mask_byte_stream.getvalue()

        if not self.dryrun:
            response = openai.Image.create_edit(
                image=image_byte_array,
                mask=mask_byte_array,
                prompt=prompt,
                n=1,
                size=f"{brush.width}x{brush.height}",
            )

            image_url = response["data"][0]["url"]
            if self.verbose:
                logger.info(f"Canvas.generate: received {image_url}")

            response = requests.get(image_url)
            image_data = response.content
            image__ = Image.open(BytesIO(image_data))
            if self.verbose:
                logger.info(
                    f"Canvas.generate: downloaded {image__.size}, {image__.mode}"
                )

            self.image.paste(image__, box)

        self.mask.paste(
            Image.new(
                "L",
                (brush.width, brush.height),
                (255,),
            ),
            box,
        )

        if self.debug_mode or self.is_jupyter:
            from IPython.display import display, clear_output

            clear_output(wait=True)

            if self.debug_mode:
                image = Image.new("RGB", (3 * brush.width, brush.height))
                image.paste(image_, (0, 0))
                image.paste(mask_, (brush.width, 0))
                image.paste(image__, (2 * brush.width, 0))
                display(self.add_signature(image))

                image = Image.new("RGB", (2 * self.width, self.height))
                image.paste(self.mask, (0, 0))
                image.paste(self.image, (self.width, 0))
                display(self.add_signature(image))
            else:
                display(self.add_signature(self.image.crop(self.box())))

        return self

    @staticmethod
    def add_signature(image):
        return Image.fromarray(
            add_signature(
                np.array(image),
                [" | ".join(object_signature())],
                [" | ".join([f"{NAME}-{VERSION}"] + host_signature())],
            )
        )

    def save(self, filename):
        box = self.box()

        mask = self.mask.crop(box)
        image = self.image.crop(box)

        image = self.add_signature(image)

        image.save(filename)
        mask.save(file.add_postfix(filename, "mask"))

        if self.debug_mode and self.is_jupyter:
            from IPython.display import display, clear_output

            clear_output(wait=True)
            display(image)

        logger.info(f"Canvas -> {filename}")
