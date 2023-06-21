import os
from typing import List, Tuple, Dict, Any
from abcli import file
import matplotlib.pyplot as plt
from openai_cli.completion.functions.generic import ai_function
from abcli import string
import abcli.logging
import logging

logger = logging.getLogger()


class i2i_function(ai_function):
    def __init__(
        self,
        *args,
        plot: bool = False,
        **kwargs,
    ):
        super().__init__(
            *args,
            output_class_name="ndarray",
            **kwargs,
        )

        self.plot = plot

    def compute(self, inputs):
        if self.function_handle is None:
            return None

        logger.info(
            "{}.compute({})".format(
                self.__class__.__name__,
                string.pretty_shape_of_matrix(inputs),
            )
        )

        output_image = super().compute(inputs)

        logger.info(
            "->{}".format(
                string.pretty_shape_of_matrix(output_image),
            )
        )

        if self.plot:
            _, axes = plt.subplots(1, 2, figsize=(10, 5))
            axes[0].imshow(inputs)
            axes[0].axis("off")
            axes[0].set_title("input image")

            axes[1].imshow(output_image)
            axes[1].axis("off")
            axes[1].set_title("output image")
            plt.subplots_adjust(wspace=0.1)
            plt.show()

        return output_image

    def generate(
        self,
        *args,
        **kwargs,
    ) -> Tuple[bool, Dict[str, Any]]:
        filename = os.path.join(
            os.getenv("HOME", ""),
            "git/blue-bracket/images/portal-34.jpg",
        )
        success, image = file.load_image(filename)
        if not success:
            return False, {"error": f"{filename} not found."}

        return super().generate(
            *args,
            validation_input=image,
            **kwargs,
        )
