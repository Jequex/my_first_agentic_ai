import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config.config import MODEL_NAME

from config.prompts import system_prompt
from config.call_function import available_functions
from config.call_function import call_function

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
    
    token_check = client.models.count_tokens(
        model=MODEL_NAME,
        contents=messages,
    )
    
    print(f'Token check - prompt tokens: {token_check.total_tokens}')
    
    if (token_check.total_tokens and token_check.total_tokens > 10000):
        print("Error: Prompt is too long and exceeds the maximum token limit.")
        return
    
    for _ in range(20):
        print(f'messages: {[m for m in messages]}')
        print(f'iteration {_}')
        
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=messages,
            config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions])
        )
        
        candidates = response.candidates
        
        if candidates and len(candidates) > 0:
            for candidate in candidates:
                if candidate.content:
                    messages.append(candidate.content)
        
        try:
            if response.function_calls and len(response.function_calls) > 0:
                for function_call in response.function_calls:
                    function_call_response = call_function(function_call, args.verbose)
                    if not function_call_response.parts:
                        raise Exception
                    if function_call_response.parts[0].function_response is None:
                        raise Exception
                    if function_call_response.parts[0].function_response.response is None:
                        raise Exception
                    if args.verbose:
                        print(f"-> {function_call_response.parts[0].function_response.response}")
                    messages.append(function_call_response)
            else:
                print(response.text)
                
        except Exception as e:
            print(f"Error processing function call response: {e}")
            return
        
        if args.verbose and response.usage_metadata:
            print(f'User prompt: {args.user_prompt}')
            print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
            print(f'Response tokens: {response.usage_metadata.candidates_token_count}')
            print(f'Total tokens: {response.usage_metadata.total_token_count}')
    
    else:
        print("Error: Maximum number of iterations reached without completing the task.")
    
    return


if __name__ == "__main__":
    main()
