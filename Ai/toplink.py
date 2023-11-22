#Receives A1loop to search after the question was refined. Gets google top link and requires user input.

import aiohttp
import asyncio
from A1Loop import main
import sys
import json
import B2loop
from urllib.parse import urlparse
import logging
import requests

import requests

async def palm_search(user_input):
    api_key = 'AIzaSyDvnKzhAEh5EnrYoy7wvS1_MMcD3pcRG6M'
    url = "https://generativelanguage.googleapis.com/v1beta3/models/text-bison-001:generateText"
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }
    data = {
        "prompt": {"text": user_input}
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as response:
            if response.status == 200:
                json_response = await response.json()
                if 'candidates' in json_response and json_response['candidates']:
                    output = json_response['candidates'][0]['output']
                    return output
            return None

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

async def google_custom_search(query, max_retries=3):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": 'AIzaSyA6kLTjTgsI28n13xFoZKVMM-PHDC4AR-I',
        "cx": 'c53f271da46c84856',
        "q": query
    } 
    for attempt in range(max_retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        top_link = data['items'][0]['link'] if 'items' in data and len(data['items']) > 0 else None
                        if top_link and is_valid_url(top_link):
                            return top_link
                    else:
                        logging.warning(f"Attempt {attempt+1}: API request failed with status {response.status}")
                        # Optionally, add a delay here if needed
        except Exception as e:
            logging.warning(f"Attempt {attempt+1} failed with error: {e}")
            # Optionally, add a delay here if needed
    return None

# user_input="top ten tech startups"

async def B2_search(user_input):
    processed_query = B2loop.main(user_input)
    top_link = await google_custom_search(processed_query)
    if top_link:
        print(json.dumps({'url': top_link}))  # Print as JSON
    else:
        print(json.dumps({'error': f"No results found or invalid URL for query: {processed_query}"}))

async def A1_search(user_input):
    """This seems to excell more than C3 at short search phrases, but I only did a few tests"""
    query = main(user_input)
    top_link = await google_custom_search(query)
    if top_link:
        print(json.dumps({'url': top_link}))  # Print as JSON
    else:
        print(json.dumps({'error': "No results found."}))


async def C3_search(user_input):
    top_link = await google_custom_search(user_input)
    if top_link:
        print(json.dumps({'url': top_link}))  # Print as JSON
    else:
        print(json.dumps({'error': "No results found."}))

# if __name__ == "__main__":
#     if len(sys.argv) > 2:
#         user_input = sys.argv[2]
#         search_method = sys.argv[1]

#         # Check if user_input is empty
#         if user_input.strip() == "":
#             print(json.dumps({'error': "Empty search term provided."}))
#         else:
#             if search_method == "A1":
#                 # asyncio.run(A1_search(user_input))
#                 result = asyncio.run(A1_search(palm_search(user_input)))
#                 if result:
#                     print(json.dumps({'output': result}))
#                 else:
#                     print(json.dumps({'error': "No results found."}))
#             elif search_method == "B2":
#                 asyncio.run(B2_search(user_input))
#             elif search_method == "C3":
#                 asyncio.run(C3_search(user_input))
#             else:
#                 print("Invalid search method. Please specify 'A1', 'B2', 'C3', or 'palm'.")
#     else:
#         print("Please provide the search method ('A1', 'B2', or 'C3') and a search query as arguments.")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        user_input = sys.argv[2]
        search_method = sys.argv[1]

        if user_input.strip() == "":
            print(json.dumps({'error': "Empty search term provided."}))
        else:
            if search_method == "A1":
                palm_result = asyncio.run(palm_search(user_input))
                if palm_result:
                    # Ensure palm_result is a string suitable for a search query
                    A1_result = asyncio.run(A1_search(palm_result))
                    if A1_result:
                        print(json.dumps({'output': A1_result}))
                    else:
                        print(json.dumps({'error': "No results found."}))
                else:
                    print(json.dumps({'error': "No results from palm search."}))
            elif search_method == "B2":
                asyncio.run(B2_search(user_input))
            elif search_method == "C3":
                asyncio.run(C3_search(user_input))
            else:
                print("Invalid search method. Please specify 'A1', 'B2', 'C3', or 'palm'.")
    else:
        print("Please provide the search method ('A1', 'B2', 'C3', or 'palm') and a search query as arguments.")

#run example:
# python toplink.py A1 "top ten tech startups"
# python toplink.py C3 "top ten tech startups"
#TODO I'm pretty sure the code below will work if you give it an API key that works.
        #please sort that out this is a pain.

#newer version I'm working on to make sure there are no static images, avoids A1's blank urls by leaning on B2's history function. 
        # B2 shouldn't ever have that problem but if it does it can just call the infer from history again since its a lot of information to go from.
        #Play with B2's history inference prompt.

# async def A1_search(user_input):
#     query = main(user_input)
#     top_link = await google_custom_search(query)
#     return top_link

# async def B2_search(user_input):
#     processed_query = B2loop.main(user_input)
#     top_link = await google_custom_search(processed_query)
#     return top_link

# async def C3_search(user_input):
#     top_link = await google_custom_search(user_input)
#     return top_link

# async def search_with_fallback(user_input):
#     # Try A1 search first
#     top_link = await A1_search(user_input)
#     if top_link:
#         return {'url': top_link}

#     # Fallback to B2 if A1 fails
#     fallback_query = B2loop.main(user_input)
#     top_link = await A1_search(fallback_query)
#     if top_link:
#         return {'url': top_link}

#     # Fallback to C3 if A1 and B2 fail
#     top_link = await C3_search(user_input)
#     if top_link:
#         return {'url': top_link}

#     return {'error': "No results found."}

# if __name__ == "__main__":
#     user_input = sys.argv[2] if len(sys.argv) > 2 else "default"
#     search_method = sys.argv[1] if len(sys.argv) > 1 else "A1"

#     if search_method == "A1":
#         result = asyncio.run(search_with_fallback(user_input))
#     elif search_method == "B2":
#         result = asyncio.run(B2_search(user_input))
#     elif search_method == "C3":
#         result = asyncio.run(C3_search(user_input))
#     else:
#         result = {'error': "Invalid search method."}

#     print(json.dumps(result))
    