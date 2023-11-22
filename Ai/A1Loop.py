#This is for A1's front end interaction, compression and search. The purpose of which is to improve a search through inference.
#This is passed to toplink for the search portion.

import openai
import sys
import asyncio
import os
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)

# Get API keys from environment variables
OPENAI_API_KEYS = os.getenv('OPENAI_API_KEYS')  # The name of the environment variable should be 'OPENAI_API_KEYS'
if not OPENAI_API_KEYS:
    raise EnvironmentError("No OpenAI API keys found in environment variable.")

OPENAI_API_KEYS = OPENAI_API_KEYS.split(';')

def get_api_key():
    get_api_key.current_key = (get_api_key.current_key + 1) % len(OPENAI_API_KEYS)
    current_key_value = OPENAI_API_KEYS[get_api_key.current_key]
    logging.info(f"Using API key: {current_key_value[:4]}...")  # Logging the first few characters for identification
    return current_key_value

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