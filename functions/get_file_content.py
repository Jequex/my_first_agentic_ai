import os
from config.config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
  
  try:
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.normpath(os.path.join(working_directory, file_path)))
    
    valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    
    if not valid_target_file:
      print(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
      return
    
    if not os.path.isfile(target_file):
      print(f'Error: "{file_path}" is not a file')
    else:
      content = ""
      with open(target_file, 'r') as f:
        content = f.read(MAX_CHARS)
        if f.read(1):  # Check if there's more content after reading MAX_READ_CHARS
          content += f'[...File {file_path} truncated: True]'
        
        print(content)
  
  except Exception as e:
    print(f'Error: {str(e)}')
    
    

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a specified file relative to the working directory, with a maximum character limit",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to read content from, relative to the working directory",
            ),
        },
    ),
)