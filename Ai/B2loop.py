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

# user_profile = f"Please determine the who, what, where, why, and how of the person that wrote these lines: {searchHistory}"

def main(user_input,search_history):
    user_profile_context = "Please determine the who, what, where, why, and how of the person that wrote these lines:"
    context1=""
    answer1 = call1(user_input, context1)

    evalUserHistory = call1(search_history, user_profile_context)
    answer2 = call1(answer1, evalUserHistory)
    # answerN1 = call1(answer1, user_profile_context)
    # answerN2 = call1(answerN1, user_profile2)
    inputN= f"Please accurately compress and translate this to a google search: {answer2}"
    answerN = call1(inputN, context1)
    answerN = answerN.strip('"')
    return answerN
print(main("chick soup", read_search_history()))