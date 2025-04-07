import json


def read_json_file(file_path):
    """
    Reads a json file from the given file path and returns its content as a Python dictionary.

    :param file_path: The path to the JSON file on the disk.
    :return: A JSON content of the JSON file.
    """
    try:
        with open(file_path, 'r') as file:
            json_file = json.load(file)
        return json_file
    except FileNotFoundError:
        raise FileNotFoundError(f"The file at path '{file_path}' was not found.")
    except Exception as e:
        raise ValueError(f"Error reading JSON file: {e}")
