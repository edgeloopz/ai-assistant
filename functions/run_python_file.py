import os

def run_python_file(working_directory, file_path):
            try:
                joined_directory = os.path.join(working_directory,file_path)
                abs_working_directory = os.path.abspath(working_directory)
                abs_directory = os.path.abspath(joined_directory)

                #If the file_path is outside of the working_directory, return a string with an error:
                if not abs_directory.startswith(abs_working_directory):
                    return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
            
            except Exception as e:
                   return f"Error: {e}"
