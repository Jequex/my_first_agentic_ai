import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config.config import MODEL_NAME

from config.prompts import system_prompt
from config.call_function import available_functions

load_dotenv()


def main():
    # print("Hello from my-first-agentic-ai!")
    api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    parser = argparse.ArgumentParser(description='Chatbot')
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions])
    )
    
    print(response.text)
    
    if args.verbose and response.usage_metadata:
        print(f'User prompt: {args.user_prompt}')
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {response.usage_metadata.thoughts_token_count}')


if __name__ == "__main__":
    main()
