# call1(user_prompt, context):
# user_profile = f"Please determine the who, what, where, why, and how of the person that wrote these lines: {searchHistory}"
    #answ2er og previously used evalUserHistory here 2nd ip #history as context, but does that work to inform better choices?
    # answerN1 = call1(answer1, user_profile_context)
    # answerN2 = call1(answerN1, user_profile2)

#Update changes to /var/www/feldspar/NewFeldspar in filezilla or if needed: restart with sudo systemctl restart nginx

import openai
import sys
import asyncio
from A1Loop import call1
import json
import requests
from requests.exceptions import RequestException
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)

def is_valid_url(url, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            response = requests.head(url, allow_redirects=True, timeout=5)
            if response.status_code == 200:
                return True
        except RequestException as e:
            logging.warning(f"URL check failed, retrying... {e}")
            retries += 1
    return False

def historical_parser():
    try:
        with open('UserDat/searchHistory.txt', 'r') as file:
            history = file.read().splitlines()
        return ', '.join(f"{index + 1}. {item}" for index, item in enumerate(history))
    except FileNotFoundError:
        return "No history file found."

def call_with_retry(user_input, context, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            return call1(user_input, context)
        except Exception as e:
            logging.warning(f"API call failed, retrying... {e}")
            retries += 1
    return "API call failed after retries"

def main(user_input):
    context1 = ""
    context2 = "Output a simple relevant google search." #The purpose of all this is to learn who someone is to provide them with the most relevant and best possible results. Use less than 20 words."

    user_profile_context = "Please determine the who, what, where, why, and how of the person that wrote these lines:"
    b2search = historical_parser()

    if b2search == "No history file found.":
        return "Error: Search history file not found."

    answer1 = call_with_retry(user_input, context1)
    evalUserHistory = call_with_retry(b2search, user_profile_context)
    history_inference = f"Considering that this is who a user is: {evalUserHistory}, please bias their latest question to who they are, what they know, and what they'd likely like to see:"
    answer2 = call_with_retry(answer1, history_inference)
    inputN = f"Please accurately compress these features: {answer2}, into one simple and reasonable google search."  #and reasonable google search the purpose of this is to learn who someone is to provide them with the most relevant and best possible results
    # inputN = f"Please accurately compress and translate this into one simple google search: {answer2}" #and reasonable google search the purpose of this is to learn who someone is to provide them with the most relevant and best possible results
    #please add a history parser duplicate function here if inputN does not return something starting with a https i.e. if it isn't a url etc:
    answerN = call_with_retry(inputN, context2)  # Updated to include word_count
    #outputs url? Should be a search query TO lookup.
    answerN = answerN.strip('"')
    return answerN

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