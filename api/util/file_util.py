import os
from typing import List


def clear_files_with_extension(directory_path: str, file_extension: str):
    """
    Remove all files with the specified extension in the given directory.

    Args:
        directory_path (str): The path to the directory to clear.
        file_extension (str): The file extension to look for (e.g., '.txt').
    """
    # Ensure the file extension starts with a dot
    if not file_extension.startswith('.'):
        file_extension = '.' + file_extension

    # Check if the directory exists
    if not os.path.exists(directory_path):
        print(f"The directory {directory_path} does not exist.")
        return

    # Iterate over all the files in the specified directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        try:
            # Check if it's a file and if it has the specified extension
            if os.path.isfile(file_path) and filename.endswith(file_extension):
                os.remove(file_path)  # Remove the file
                print(f"Deleted: {file_path}")
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')


def get_files_with_extension(directory_path: str, file_extension: str) -> List[str]:
    """
    Get a list of full file paths for all files with the specified extension in the given directory.

    Args:
        directory_path (str): The path to the directory to search.
        file_extension (str): The file extension to look for (e.g., '.txt').

    Returns:
        List[str]: A list of full file paths for files with the specified extension.
    """
    # Ensure the file extension starts with a dot
    if not file_extension.startswith('.'):
        file_extension = '.' + file_extension

    # Initialize an empty list to store file paths
    file_paths = []

    # Check if the directory exists
    if not os.path.exists(directory_path):
        print(f"The directory {directory_path} does not exist.")
        return file_paths

    # Iterate over all the files in the specified directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        # Check if it's a file and if it has the specified extension
        if os.path.isfile(file_path) and filename.endswith(file_extension):
            file_paths.append(file_path)  # Add the full file path to the list

    return file_paths

if __name__ == '__main__':
    # clear_files_with_extension('/path/to/directory', '.txt')
    result = get_files_with_extension('/Users/gemushen/root/jinx/api/tmp', '.webm')
    print(result)
