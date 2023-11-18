#Receives A1loop to search after the question was refined. Gets google top link and requires user input.

import aiohttp
import asyncio
from A1Loop import main
import sys
import json
import B2loop

async def google_custom_search(query):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": 'AIzaSyA6kLTjTgsI28n13xFoZKVMM-PHDC4AR-I',
        "cx": 'c26f4856565da4bf3',
        "q": query
    } 
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            data = await response.json()
            # Extract the top link from the response
            top_link = data['items'][0]['link'] if 'items' in data and len(data['items']) > 0 else None
            return top_link

# user_input="top ten tech startups"

async def A1_search(user_input):
    """This seems to excell more than C3 at short search phrases, but I only did a few tests"""
    query = main(user_input)
    top_link = await google_custom_search(query)
    if top_link:
        print(json.dumps({'url': top_link}))  # Print as JSON
    else:
        print(json.dumps({'error': "No results found."}))

async def B2_search(user_input):
    processed_query = B2loop.main(user_input)
    top_link = await google_custom_search(processed_query)
    if top_link:
        print(json.dumps({'url': top_link}))  # Print as JSON
    else:
        # Handle the case where no valid URL is found
        print(json.dumps({'error': f"No results found for query: {processed_query}"}))

async def C3_search(user_input):
    top_link = await google_custom_search(user_input)
    if top_link:
        print(json.dumps({'url': top_link}))  # Print as JSON
    else:
        print(json.dumps({'error': "No results found."}))

if __name__ == "__main__":
    if len(sys.argv) > 2:
        user_input = sys.argv[2]
        search_method = sys.argv[1]

        if search_method == "A1":
            asyncio.run(A1_search(user_input))
        elif search_method == "B2":
            asyncio.run(B2_search(user_input))
        elif search_method == "C3":
            asyncio.run(C3_search(user_input))
        else:
            print("Invalid search method. Please specify 'A1', 'B2', or 'C3'.")
    else:
        print("Please provide the search method ('A1', 'B2', or 'C3') and a search query as arguments.")

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
    