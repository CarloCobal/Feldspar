#This is for A1's front end interaction, compression and search. The purpose of which is to improve a search through inference.
#This is passed to toplink for the search portion.

import openai
import os
import logging
# from dotenv import load_dotenv

# Load .env file from the specified path
# load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

# Setup basic logging
logging.basicConfig(level=logging.INFO)

# Get API keys from environment variables
OPENAI_API_KEYS = os.getenv('OPENAI_API_KEYS')
if not OPENAI_API_KEYS:
    raise EnvironmentError("No OpenAI API keys found in environment variable.")

OPENAI_API_KEYS = OPENAI_API_KEYS.split(';')

# OPENAI_API_KEYS = "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"
def get_api_key():
    get_api_key.current_key = (get_api_key.current_key + 1) % len(OPENAI_API_KEYS)
    return OPENAI_API_KEYS[get_api_key.current_key]

get_api_key.current_key = 0

def call1(user_prompt, context):
    """context prompt with adjustable bias"""
    # Set the API key for this call
    openai.api_key = get_api_key()

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {'role': 'system', 'content': context},
            {'role': 'user', 'content': user_prompt}
        ],
        max_tokens=150
    )
    return response['choices'][0]['message']['content']
# print(call1("hello",""))
# print(call1("hello world", ""))
def main(user_input):
    # Check if user_input is empty and set a default prompt if it is
    if not user_input.strip():
        user_input = "please find me a random website"

    context1 = f"Please find the best uses for, or best versions of {user_input}"
    answer1 = call1(user_input, context1)
    input2 = f"Please accurately compress and translate this to a google search: {answer1}"
    answer2 = call1(input2, context1)
    answer2 = answer2.strip('"')
    return answer2

# Example usage (uncomment and modify as needed for testing)
# user_input = "top ten tech startups"
# user_input = ""
# result = main(user_input)
# print(result)