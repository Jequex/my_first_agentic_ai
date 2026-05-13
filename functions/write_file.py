import os
from google.genai import types

def write_file(working_directory, file_path, content):
  try:
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.normpath(os.path.join(working_directory, file_path)))
    
    valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    
    if not valid_target_file:
      print(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
      return
    
    if os.path.isdir(target_file):
      print(f'Error: Cannot write to "{file_path}" as it is a directory')
      return
    
    os.makedirs(os.path.dirname(target_file), exist_ok=True)
    
    with open(target_file, 'w') as f:
      f.write(content)
      print(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')
  
  except Exception as e:
    print(f'Error: {str(e)}')


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file relative to the working directory, creating any necessary directories",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write content to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
    ),
)