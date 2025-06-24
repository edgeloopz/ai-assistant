import os

def get_files_info(working_directory, directory=None):

    try:

        #if directory is outside working directory return string with Error
        joined_directory = os.path.join(working_directory,directory)
        abs_working_directory = os.path.abspath(working_directory)
        abs_directory = os.path.abspath(joined_directory)
    
        if not abs_directory.startswith(abs_working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
        #if directory argument is not a directory return string with error
        if not os.path.isdir(abs_directory):
            return f'Error: "{directory}" is not a directory'
    
        #format output
        directory_list = os.listdir(abs_directory)
        return_list = []
        for item in directory_list:
            item_directory = os.path.join(abs_directory,item)
            name = item
            file_size = os.path.getsize(item_directory)
            is_path = os.path.isdir(item_directory)
            return_list.append(f"- {name}: file_size={file_size}, is_dir={is_path}")
        
        return "\n".join(return_list)
    
    except Exception as e:
        return f"Error: {e}"



    