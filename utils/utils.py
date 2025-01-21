"""
This script defines a function to delete a file from the file system.
It is useful in scenarios where you need to programmatically remove files,
such as cleaning up temporary files, managing logs, or deleting unwanted data.
The function ensures that the file exists before attempting to delete it,
preventing potential errors.
"""

import os  # Import the 'os' module to interact with the operating system for file operations.


def delete_file(file_path):
    """
    Delete a file from the file system if it exists.
    Args:
        file_path (str): The path of the file to be deleted.
    """

    if file_path and os.path.exists(file_path):
        # Check if 'file_path' is not None or empty and if the file exists at the specified path.

        os.remove(file_path)
        # Remove the file from the file system using 'os.remove()'.
