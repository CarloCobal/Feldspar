#Receives A1loop to search after the question was refined. Gets google top link and requires user input.
import aiohttp
import asyncio
from A1Loop import main
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

async def search(user_input):
    query = main(user_input)
    print(f"Query from main: '{query}'")

    # Use this query in the Google custom search
    top_link = await google_custom_search(query)
    if top_link:
        print(top_link)
    else:
        print("No results found.")

asyncio.run(search(user_input="top ten tech startups"))
