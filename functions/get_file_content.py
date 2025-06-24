import os

def get_file_content(working_directory, file_path):

    try:
        #If the file_path is outside the working_directory, return a string with an error:
        joined_directory = os.path.join(working_directory,file_path)
        abs_working_directory = os.path.abspath(working_directory)
        abs_directory = os.path.abspath(joined_directory)
    
        if not abs_directory.startswith(abs_working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        #If the file_path is not a file, again, return an error string:
        if not os.path.isfile(abs_directory):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        #Read the file and return its contents as a string.
        #If the file is longer than 10000 characters, truncate it to 10000 characters
        MAX_CHARS = 10000

        with open(abs_directory, "r") as f:
            file_content_string = f.read(MAX_CHARS)

        if len(file_content_string) == MAX_CHARS:
            file_content_string = file_content_string + f'...File "{abs_directory}" truncated at 10000 characters'
            return file_content_string
    
        return file_content_string

    except Exception as e:
        return f"Error: {e}"
