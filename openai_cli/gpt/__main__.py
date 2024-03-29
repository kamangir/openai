import argparse
from openai_cli import VERSION
from openai_cli.gpt import NAME
from openai_cli.gpt.chat import chat_with_openai, list_models
from openai_cli.logger import logger

parser = argparse.ArgumentParser(NAME, description=f"{NAME}-{VERSION}")
parser.add_argument(
    "task",
    type=str,
    help="chat_with_openai|list_models",
)
parser.add_argument(
    "--object_path",
    type=str,
    default="",
)
parser.add_argument(
    "--model_name",
    type=str,
    default="gpt-3.5-turbo",
    help='"gpt list_models".',
)
parser.add_argument(
    "--log",
    type=int,
    default=1,
    help="0|1",
)
args = parser.parse_args()

success = False
if args.task == "chat_with_openai":
    success = chat_with_openai(
        object_path=args.object_path,
        model_name=args.model_name,
    )
elif args.task == "list_models":
    success = True
    list_models(log=bool(args.log))
else:
    logger.error(f"-{NAME}: {args.task}: command not found.")

if not success:
    logger.error(f"-{NAME}: {args.task}: failed.")
