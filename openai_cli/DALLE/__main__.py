import argparse
from abcli import file
from tqdm import tqdm
from openai_cli.DALLE import NAME
from openai_cli.DALLE.canvas import Canvas
from openai_cli.DALLE.brush import RandomWalkBrush, TilingBrush
from openai_cli import VERSION
from abcli import logging
import logging

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(NAME, description=f"{NAME}-{VERSION}")
parser.add_argument(
    "task",
    type=str,
    help="render",
)
parser.add_argument(
    "--filename",
    type=str,
)
parser.add_argument(
    "--brush",
    type=str,
    help="tiling|randomwalk",
    default="tiling",
)
parser.add_argument(
    "--lines",
    type=int,
    help="-1: disable",
)
parser.add_argument(
    "--verbose",
    type=int,
    help="0|1",
    default=0,
)
parser.add_argument(
    "--dryrun",
    type=int,
    help="0|1",
    default=1,
)
args = parser.parse_args()

success = False
if args.task == "render":
    canvas = Canvas(
        dryrun=args.dryrun == 1,
        verbose=args.verbose == 1,
    )

    success = True
    if args.brush == "tiling":
        brush = TilingBrush(canvas)
    elif args.brush == "randomwalk":
        brush = RandomWalkBrush(canvas)
    else:
        success = False

    if success:
        success, content = file.load_text(args.filename)

    if success:
        content = [line for line in content if line]

        if args.lines != -1:
            content = content[: args.lines]

        logger.info(f"loaded {len(content)} line(s) of text.")

        image_filename = file.set_extension(args.filename, "png")
        for index in tqdm(range(len(content))):
            canvas.generate(brush, content[index])
            brush.move(canvas)

            if args.verbose:
                canvas.save(file.add_postfix(image_filename, f"{index:05d}"))

        canvas.save(image_filename)
else:
    logger.error(f"-{NAME}: {args.task}: command not found.")

if not success:
    logger.error(f"-{NAME}: {args.task}: failed.")
