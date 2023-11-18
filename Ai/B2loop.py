import openai
import sys
import asyncio
from A1Loop import call1
import json

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

def main(user_input):
    context1=""
    user_profile_context = "Please determine the who, what, where, why, and how of the person that wrote these lines:"
    b2search = historical_parser()
    answer1 = call1(user_input, context1)
    evalUserHistory = call1(b2search, user_profile_context)
    history_inference = f"Considering that this is who a user is: {evalUserHistory}, please bias their latest question to who they are, what they know, and what they'd likely like to see:"
    answer2 = call1(answer1, history_inference)#was previously evalUserHistory here 2nd ip #history as context, but does that work to inform better choices?
    # answerN1 = call1(answer1, user_profile_context)
    # answerN2 = call1(answerN1, user_profile2)
    inputN= f"Please accurately compress and translate this to a simple google search: {answer2}"
    answerN = call1(inputN, context1)
    answerN = answerN.strip('"')
    return answerN
# print(main("are all the things here?"))

if __name__ == "__main__":
    user_input = sys.argv[1] if len(sys.argv) > 1 else "default"
    result = main(user_input)
    print(json.dumps({"result": result}))

#outputs:
# Understanding limitations of data context-based query details
# Coding insights, programming languages, best practices, technology trends, creating engaging content, improving writing skills, exploring writing styles
"""From this data: 
hello world
hows life?
whats happening?
what's new
beautiful music
a new type of search
jallopy
are all the things here?
"""