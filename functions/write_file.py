import os

def write_file(working_directory, file_path, content):
        try:
            joined_directory = os.path.join(working_directory,file_path)
            abs_working_directory = os.path.abspath(working_directory)
            abs_directory = os.path.abspath(joined_directory)

            #If the file_path is outside of the working_directory, return a string with an error:
            if not abs_directory.startswith(abs_working_directory):
                return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
            
            if not os.path.exists(os.path.dirname(abs_directory)):
                 os.makedirs(os.path.dirname(abs_directory)) #gets path directory name

            with open(abs_directory, "w") as f:
                f.write(content)
                
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
            
        except Exception as e:
             return f"Error: {e}"