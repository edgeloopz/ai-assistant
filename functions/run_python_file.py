import os
import subprocess

def run_python_file(working_directory, file_path):
            try:
                joined_directory = os.path.join(working_directory,file_path)
                abs_working_directory = os.path.abspath(working_directory)
                abs_directory = os.path.abspath(joined_directory)

                #If the file_path is outside of the working_directory, return a string with an error:
                if not abs_directory.startswith(abs_working_directory):
                    return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
                
                if not os.path.exists(abs_directory):
                    return f'Error: File "{file_path}" not found.'
                
                if abs_directory[-3:] != ".py":
                      return f'Error: "{file_path}" is not a Python file.'
                
                output = subprocess.run(["python3",abs_directory], capture_output=True,timeout = 30,cwd = abs_working_directory)
                stdout = output.stdout.decode('utf-8')
                stderr = output.stderr.decode('utf-8')
                stdout = stdout.strip()
                stderr = stderr.strip()

                if stdout == "" and stderr == "":
                    return "No output produced."
                
                if output.returncode != 0:
                      return f"STDOUT: {stdout}\nSTDERR: {stderr}\n" + f"Process exited with code {output.returncode}"
                
                return f"STDOUT: {stdout}\nSTDERR: {stderr}"
            
            
            except Exception as e:
                   return f"Error: executing Python file: {e}"
            
