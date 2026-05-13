import os
from google.genai import types


def get_files_info(working_directory, directory="."):
  try:
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.normpath(os.path.join(working_directory, directory)))
    
    # print(f'working_dir_abs: {working_dir_abs}, target_dir: {target_dir}')
    
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    # print(f'valid_target_dir: {valid_target_dir}, working_dir_abs: {working_dir_abs}, target_dir: {target_dir}')
    
      
    directory_name = ""
    
    if (directory == "."):
      directory_name = "current"
    else:
      directory_name = directory
      
      
    print(f'Result for {directory_name} directory')
    
    
    if not valid_target_dir:
      print(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
      return
    
    if not os.path.isdir(target_dir):
      print(f'Error: "{directory}" is not a directory')
    else:
      print(f'Success: "{directory}" is within the working directory')
      
    
    for item in os.listdir(target_dir):
      print(f'{item}: file_size={os.path.getsize(os.path.join(target_dir, item))} bytes, is_dir={os.path.isdir(os.path.join(target_dir, item))}')
      
  
  except Exception as e:
    print(f'Error: {str(e)}')
  
  
  
  
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)