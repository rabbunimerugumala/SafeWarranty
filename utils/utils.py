import os
# Import the 'os' module to interact with the operating system, allowing us to perform file operations like checking if a file exists and deleting it.

def delete_file(file_path):
    """Delete a file from the file system if it exists."""
    # This is the function definition. It takes one argument, 'file_path', which is the path of the file to be deleted.

    if file_path and os.path.exists(file_path):
        # The 'if' statement checks if 'file_path' is not None or empty, and if the file actually exists at the specified path using os.path.exists.

        os.remove(file_path)
        # If the file exists, it is deleted using os.remove(), which removes the file from the file system.
