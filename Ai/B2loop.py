import openai
import sys
import asyncio
from A1Loop import call1

# call1(user_prompt, context):
# user_profile = f"Please determine the who, what, where, why, and how of the person that wrote these lines: {searchHistory}"

def historical_parser():
    with open('UserDat/searchHistory.txt', 'r') as file:
        history = file.read().splitlines()

    # Concatenate the list into a numbered string
    numbered_history = ', '.join(f"{index + 1}. {item}" for index, item in enumerate(history))
    return numbered_history

searchHistory = historical_parser()

# print(searchHistory)  # For testing

def main(user_input,search_history):
    context1=""
    user_profile_context = "Please determine the who, what, where, why, and how of the person that wrote these lines:"
    
    answer1 = call1(user_input, context1)
    evalUserHistory = call1(search_history, user_profile_context)
    history_inference = f"Considering that this is who a user is: {evalUserHistory}, please bias their latest question to who they are, what they know, and what they'd likely like to see:"
    answer2 = call1(answer1, history_inference)#was previously evalUserHistory here 2nd ip #history as context, but does that work to inform better choices?
    # answerN1 = call1(answer1, user_profile_context)
    # answerN2 = call1(answerN1, user_profile2)
    inputN= f"Please accurately compress and translate this to a google search: {answer2}"
    answerN = call1(inputN, context1)
    answerN = answerN.strip('"')
    return answerN
print(main("chick soup", historical_parser()))



