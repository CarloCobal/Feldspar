import openai
import sys
import asyncio
from A1Loop import call1

# call1(user_prompt, context):


def read_search_history():
    with open('UserDat/searchHistory.txt', 'r') as file:
        history = file.read().splitlines()
    return history

searchHistory = read_search_history()
print(searchHistory)  # For testing


# def main(user_input):
#     context1=""
#     answer1 = call1(user_input, context1)
#     input2= f"Please accurately compress and translate this to a google search: {answer1}"
#     answer2 = call1(input2, context1)
#     answer2 = answer2.strip('"')
#     return answer2
