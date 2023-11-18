#Receives A1loop to search after the question was refined. Gets google top link and requires user input.
import aiohttp
import asyncio
from A1Loop import main
import sys
import json

async def google_custom_search(query):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": 'AIzaSyCqrnzM-GLKIZalq_AmA3uvpuchiZJZQLQ',
        "cx": '94eb91fc4b7e143e4',
        "q": query
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            data = await response.json()
            # Extract the top link from the response
            top_link = data['items'][0]['link'] if 'items' in data and len(data['items']) > 0 else None
            return top_link

user_input="top ten tech startups"

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

if __name__ == "__main__":
    if len(sys.argv) > 2:
        user_input = sys.argv[2]
        search_method = sys.argv[1]

        if search_method == "A1":
            asyncio.run(A1_search(user_input))
        elif search_method == "C3":
            asyncio.run(C3_search(user_input))
        else:
            print("Invalid search method. Please specify 'A1' or 'C3'.")
    else:
        print("Please provide the search method ('A1' or 'C3') and a search query as arguments.")

#run example:
# python toplink.py A1 "top ten tech startups"
# python toplink.py C3 "top ten tech startups"
