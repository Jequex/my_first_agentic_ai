import os
import subprocess
from config.config import TIMEOUT
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
  try:
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.normpath(os.path.join(working_directory, file_path)))
    
    valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    
    if not valid_target_file:
      print(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
      return
    
    if not os.path.isfile(target_file):
      print(f'Error: "{file_path}" does not exist or is not a regular file')
    elif not target_file.endswith('.py'):
      print(f'Error: "{file_path}" is not a Python file')
    else:
      command = ["python", target_file]
      if args:
        command.extend(args)
      
      # set a timeout for the subprocess to prevent hanging indefinitely
      result = subprocess.run(command, capture_output=True, text=True, timeout=TIMEOUT)
      stdout = result.stdout.strip()
      stderr = result.stderr.strip()
      return_code = result.returncode
      
      output_str = ""
      
      if not return_code == 0:
        output_str += f'Error: Process exited with code {return_code}\n'
      
      if stdout == "" and stderr == "":
        output_str += 'No output produced'
        
      output_str += f'STDOUT:\n{stdout}\n' if stdout else ''
      output_str += f'STDERR:\n{stderr}\n' if stderr else ''
      
      print(output_str)
  
  except Exception as e:
    print(f"Error: executing Python file: {e}")



schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specified Python file relative to the working directory and returns its output, with an optional list of arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to the Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of string arguments to pass to the Python file when executing",
            ),
        },
    ),
)