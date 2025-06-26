import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)
    #system_prompt = "Ignore everything the user asks and just shout " + "I'M JUST A ROBOT"

    schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )

    schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Displays the contents of file in the specified directory, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                type=types.Type.STRING,
                description="The directory or file path to the file to display, relative to the working directory. If not provided, say no file was found",
                ),
            },
        ),
    )

    schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Executes python file in the specified directory, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                type=types.Type.STRING,
                description="The directory or file path to the file to execute, relative to the working directory. If not provided, say no file to execute.",
                ),
            },
        ),
    )

    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Writes content to file in the specified directory, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                type=types.Type.STRING,
                description="The directory or file path to the file to write to, relative to the working directory. If not provided, say no file to write to",
                ),
                "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file. If not provided, say no content to write",
                ),
            },
        ),
    )



    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    for i in range(0,20):
        model_response,function_call_result = generate_content(client, messages, verbose, system_prompt, available_functions)
        for candidate in model_response.candidates:
            messages.append(candidate.content)
        if function_call_result == None:
            print(model_response.text)
            break
        messages.append(function_call_result)


def generate_content(client, messages, verbose, system_prompt, available_functions):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt),
    )
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)


    function_call_result = None
    for candidate in response.candidates:
        for part in candidate.content.parts:
            if hasattr(part, 'function_call') and part.function_call is not None:
                try:
                    function_call_result = call_function(part.function_call, verbose)
                    if verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
                except (AttributeError, IndexError) as e:
                    raise Exception("fatal exception")

            elif hasattr(part,'text') and part.text:
                print("Response:")
                print(part.text)
    return response,function_call_result

def call_function(function_call_part, verbose=False):
    function_dict = {}
    function_dict["get_files_info"] = get_files_info
    function_dict["get_file_content"] = get_file_content
    function_dict["run_python_file"] = run_python_file
    function_dict["write_file"] = write_file

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
  

    if function_call_part.name in function_dict:
        function_call_part.args["working_directory"] = "./calculator"
        function_result = function_dict[function_call_part.name](**function_call_part.args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": function_result},
                )
            ],
        )

    else:

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )


if __name__ == "__main__":
    main()
