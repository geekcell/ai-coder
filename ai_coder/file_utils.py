import os
import shutil


def clear_output_directory(output_directory: str):
    """
    Clear the output directory of all files and folders.
    """
    for file in os.listdir(output_directory):
        file_path = os.path.join(output_directory, file)
        if os.path.isfile(file_path):
            os.unlink(file_path)
        else:
            shutil.rmtree(file_path)


def write_to_file(file_path: str, contents: str):
    """
    Write the contents to the file path. If the file path doesn't exist, create it.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write(contents)
