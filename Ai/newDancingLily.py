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

context2 = "Output a simple relevant google search." #The purpose of all this is to learn who someone is to provide them with the most relevant and best possible results. Use less than 20 words."

def athruc1(user_input):
    contextA = "Please consider the user input and output something useful"
    
    ans1 = call1(user_input, contextA)
    ans2 = call1(ans1, context2)
    ans2 = ans2.strip('"')
    return ans2

def athruc2(user_input):
    b2search = historical_parser()
    print(type(b2search))
    if b2search == "No history file found.":
        return "Error: Search history file not found."
    the_user = "These are some things about the user:" + b2search
    user_profile_context = "Please consider who the user is and output something related to them."
    ans1 = call1(the_user, user_profile_context)
    ans2 = call1(ans1, context2)
    ans2 = ans2.strip('"')
    return ans2
#still is outdated and doesn't consider recency. Hmm.
# print(athruc2("hello world"))

def athruc3(user_input):
    c3search = historical_parser()
    print(type(c3search))
    if c3search == "No history file found.":
        return "Error: Search history file not found."
    
    the_user = "These are some things about the user:" + c3search
    user_profile_context = "Please consider the user input and output something fun related to what they want."
    ans1 = call1(the_user, user_profile_context)
    ans2 = call1(ans1, context2)
    ans2 = ans2.strip('"')
    return ans2

#old c3
# def athruc3(user_input):
    # contextC = "Please consider the user input and output something fun related to what they want."
    # ans1 = call1(user_input, contextC)
    # ans2 = call1(ans1, context2)
    # ans2 = ans2.strip('"')
    # return ans2


# "more realistic":
# These are some things that a user has looked up, please take them into consideration: "how to find a girlfriend in healdsburg?
# openai
# secure website hosting
# how do profile systems work on webhosts?
# things to do in sebastopol
# 1 week in japan
# shibuya
# 1 month in norway
# Best winter coat for travel
# best webhosting service that protects intellectual property.
# welcome center
# word search puzzles
# games for seniors
# senior living
# early morning risers
# japan
# Hello world
# Hello world
# ghost of sparta" Considering all that, please output something and fun related to what they want.