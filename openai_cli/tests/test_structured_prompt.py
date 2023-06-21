import os.path
from openai_cli.completion.prompts.structured import structured_prompt
from abcli import file


def test_structured_prompt():
    prompt = structured_prompt(
        inputs=["a number"],
        returns=["that number plus 12"],
        requirements=[
            "returns 0 if the input is less than 10",
        ],
    )

    text = prompt.create("abc").replace("\n", "  ")
    while "  " in text:
        text = text.replace("  ", " ")

    assert (
        text
        == "Write a python function named abc that inputs a number and returns 0 if the input is less than 10 and returns that number plus 12."
    )
