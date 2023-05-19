import os
from argparse import ArgumentParser
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chat_models.base import BaseChatModel
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.output_parsers import CommaSeparatedListOutputParser
from ai_coder.file_utils import clear_output_directory, write_to_file
from ai_coder.prompts import (
    ListFilesPromptTemplate,
    GenerateCodePromptTemplate,
    SharedDepsPromptTemplate,
)

load_dotenv()

parser = ArgumentParser()
parser.add_argument(
    "-l",
    "--lang",
    type=str,
    default="python",
    help="programming language/framework to use",
)

parser.add_argument(
    "-p",
    "--prompt",
    type=str,
    help="prompt to use to describe the program. It can also be a path to a Markdown file (.md)",
    required=True,
)

parser.add_argument(
    "-o",
    "--output",
    type=str,
    default="./output",
    help="output directory to write the generated code to",
)


def generate_program_file(filepath: str, chat_model: BaseChatModel, **kwargs):
    prompt = GenerateCodePromptTemplate(
        input_variables=[
            "program_description",
            "files_to_create",
            "shared_dependencies",
            "file",
        ],
    )

    chat_prompt = ChatPromptTemplate.from_messages(
        [HumanMessagePromptTemplate(prompt=prompt)]
    )

    output = chat_model(
        chat_prompt.format_prompt(file=filepath, **kwargs).to_messages()
    )
    write_to_file(filepath, output.content)


def main(program_description: str, **kwargs):
    prompt = ListFilesPromptTemplate(
        input_variables=["program_description", "language_or_framework"],
    )

    language_or_framework = kwargs["language_or_framework"] or "python"
    output_directory = kwargs["output_directory"] or "./output"

    print("Hello, I'm your friendly AI coder 🤖\n")
    print("Here's what you want me to create:")
    print("\033[92m" + program_description + "\033[0m\n")
    print(
        "The chosen language/framework is: \033[92m"
        + language_or_framework.title()
        + "\033[0m\n"
    )

    chat_prompt = ChatPromptTemplate.from_messages(
        [HumanMessagePromptTemplate(prompt=prompt)]
    )
    chat_model = ChatOpenAI(temperature=0.0, client=None)

    output = chat_model(
        chat_prompt.format_prompt(
            program_description=program_description,
            language_or_framework=language_or_framework,
        ).to_messages()
    )

    output_parser = CommaSeparatedListOutputParser()

    # Filter out whitespace and empty strings
    files_to_create = list(
        filter(
            lambda x: x != "",
            map(lambda x: x.strip(), output_parser.parse(output.content)),
        )
    )

    prompt = SharedDepsPromptTemplate(
        input_variables=["program_description", "files_to_create"],
    )
    chat_prompt = ChatPromptTemplate.from_messages(
        [HumanMessagePromptTemplate(prompt=prompt)]
    )
    shared_dependencies = chat_model(
        chat_prompt.format_prompt(
            program_description=program_description,
            files_to_create=files_to_create,
        ).to_messages()
    )

    print("Here's the list of files I'll create for you in " + output_directory + ":")
    print("\033[94m" + "\n".join(files_to_create) + "\033[0m\n")

    if os.path.exists(output_directory):
        print(
            "The output directory already exists. Do you want me to clear it? (y/n) ",
            end="",
        )
        if input().lower() == "y":
            clear_output_directory(output_directory)
        else:
            print("Aborting...")
            exit(1)

    print("\nGenerating files...")
    for idx, file in enumerate(files_to_create):
        current = idx + 1
        overall = len(files_to_create)
        print(f"({current:02d}/{overall:02d}) \033[94m{file}\033[0m ...", end=" ")
        generate_program_file(
            os.path.join(output_directory, file),
            chat_model,
            program_description=program_description,
            files_to_create=files_to_create,
            shared_dependencies=shared_dependencies.content,
        )
        print("done")


if __name__ == "__main__":
    args = parser.parse_args()

    # if the prompt is a path to a Markdown file, read from file
    prompt = args.prompt
    if prompt.endswith(".md"):
        with open(args.prompt, "r") as f:
            prompt = f.read()

    main(prompt, language_or_framework=args.lang, output_directory=args.output)
