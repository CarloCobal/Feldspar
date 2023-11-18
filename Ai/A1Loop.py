#This is for A1's front end interaction, compression and search. The purpose of which is to improve a search through inference.
#This is passed to toplink for the search portion.
import openai
import sys
import asyncio

openai.api_key = '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'

def call1(user_prompt, context):
    """context prompt with adjustable bias"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {'role': 'system', 'content': context},

            {'role': 'user', 'content': user_prompt}
        ],
        max_tokens=150
    )
    return response['choices'][0]['message']['content']

# user_input = "top ten tech startups"
# user_input = "What is a neural network llm?"

def main(user_input):
    context1=""
    answer1 = call1(user_input, context1)
    input2= f"Please accurately compress and translate this to a google search: {answer1}"
    answer2 = call1(input2, context1)
    answer2 = answer2.strip('"')
    return answer2
