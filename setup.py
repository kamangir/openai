from openai_commands import NAME, VERSION, DESCRIPTION
from blueness.pypi import setup

setup(
    filename=__file__,
    repo_name="openai-cli",
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    packages=[NAME],
)
