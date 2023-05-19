from typing import Optional
from langchain.prompts import StringPromptTemplate
from langchain.output_parsers import CommaSeparatedListOutputParser

_LIST_FILES_TEMPLATE = """
You are an AI coder who creates runnable code based on a user's description of a program.

The program description is as follows:
{program_description}

With that given description, you create an exhaustive list of file paths that the user would write to create the program.
You only return the list of file paths needed to create the program, not the contents of the files.
Keep the number of files to a minimum and the overall program as simple as possible. Every file you create must be must be used in the program, no more and no less.

As the program should be created in {language_or_framework}, you must also include at least one file {deps_filename} that describes all dependencies of the program. You must however not include any files of the dependencies themselves.

You must also include all necessary configuration and auxiliary code file paths to compile and/or run the program in or with {language_or_framework}.

Do not include any extra information, explanations, or descriptions. Just the file paths.

{format_instructions}
"""


class ListFilesPromptTemplate(StringPromptTemplate):
    @classmethod
    def get_deps_filename(cls, language_or_framework: str) -> Optional[str]:
        """
        Returns the filename of the dependencies file for the given language or framework.
        """
        match language_or_framework.lower():
            case "python" | "flask" | "fastapi" | "django":
                return "requirements.txt"
            case "node" | "nodejs" | "javascript" | "typescript" | "nestjs" | "express" | "react" | "vue" | "nextjs":
                return "package.json"
            case "java" | "spring" | "springboot" | "spring-boot":
                return "pom.xml"
            case "php" | "laravel" | "symfony":
                return "composer.json"
            case "go" | "golang":
                return "go.mod"
            case _:
                return None

    def format(self, **kwargs) -> str:
        deps_filename = self.get_deps_filename(kwargs["language_or_framework"])
        if deps_filename is None:
            deps_filename = ""

        output_parser = CommaSeparatedListOutputParser()

        return _LIST_FILES_TEMPLATE.format(
            deps_filename=deps_filename,
            format_instructions=output_parser.get_format_instructions(),
            **kwargs,
        )


_SHARED_DEPS_TEMPLATE = """
You are an AI coder who creates runnable code based on a user's description of a program.

The program description is as follows:
{program_description}

The files we have determined are necessary to create the program are:
{files_to_create}

Now that we have the list of files, we need to understand what dependencies they share.
Please name and briefly describe what is shared between the files we are generating, including exported variables, data schemas, id names of every DOM elements that javascript functions will use, message names, and function names.
"""


class SharedDepsPromptTemplate(StringPromptTemplate):
    def format(self, **kwargs) -> str:
        return _SHARED_DEPS_TEMPLATE.format(**kwargs)


_GENERATE_CODE_TEMPLATE = """
You are an AI coder who creates runnable code based on a user's description of a program.

The program description is as follows:
{program_description}

The files we have determined are necessary to create the program are:
{files_to_create}

The shared dependencies between the files are:
{shared_dependencies}

We have broken up the program into per-file generation.
For now our job is is to generate code for the following file: {file}

You must generate valid code for the given file and file type, and only return the code that is necessary to create the program.
Do not add any extra information, explanations, or descriptions and just return the code as a string.

It is important that you have consistent filenames if you reference other files in your code.

Every line of code you generate must be a valid line of code in the given programming language. Do not include code fences or comments.

Bad response:
```javascript
console.log("bad")
```

Good response:
console.log("good")

Begin generating the code now.
"""


class GenerateCodePromptTemplate(StringPromptTemplate):
    def format(self, **kwargs) -> str:
        return _GENERATE_CODE_TEMPLATE.format(**kwargs)
