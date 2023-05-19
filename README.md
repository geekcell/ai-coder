# ai_coder

An experimental code generation tool powered by OpenAI's ChatGPT. It is quite heavily inspired by [smol-ai/developer](https://github.com/smol-ai/developer), but uses [LangChain](https://python.langchain.com/en/latest/) under the hood instead of [open-ai](https://github.com/openai/openai-python) directly.

## Table of contents

- [Installation](#installation)
- [Run the example](#run-the-example)
- [Usage](#usage)
- [Limitations](#limitations)
- [License](#license)
- [Authors](#authors)

## Installation

Copy `.env.example` to `.env` and enter your OpenAI API key. Without an API key, you won't be able to generate any output.

To install the project dependencies, you need to have Poetry installed. Run the following command to install Poetry:

```bash
pip install poetry
```

Once Poetry is installed, you can navigate to the project directory and run the following command to install the project dependencies:

```bash
poetry install
```

## Run the example

```bash
poetry run python main.py -p examples/hello-world.md -l nodejs
```

## Usage

To run the project, you can use the following command:

```bash
poetry run python main.py -p path/to/prompt.md [-l python] [-o ./output]
```

```
usage: main.py [-h] [-l LANG] -p PROMPT [-o OUTPUT]

options:
  -h, --help            show this help message and exit
  -l LANG, --lang LANG  programming language/framework to use
  -p PROMPT, --prompt PROMPT
                        prompt to use to describe the program. It can also be a path to a Markdown file (.md)
  -o OUTPUT, --output OUTPUT
                        output directory to write the generated code to
```

## Limitations

Since we are still waiting for beta access to GPT-4, the current version has been developed with the `gpt-3.5-model` model in mind. The first experimental results are quite promising, but this does not always produce perfectly usable or consistent code. We expect a significant improvement of the results with access to GPT-4.

If you already have access, you currently have to manually update the corresponding model in `main.py`.

```diff
--chat_model = ChatOpenAI(temperature=0.0, client=None)
++chat_model = ChatOpenAI(temperature=0.0, model_name="gpt-4" client=None)
```

## License

This project is licensed under the terms of the [MIT](./LICENSE) license.

## Authors

- [Pascal Cremer](https://github.com/b00giZm) (<pascal.cremer@geekcell.io>)
