import aiohttp
import asyncio

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

# Example usage
async def main():
    query = "example search query"  # Replace with your actual query
    top_link = await google_custom_search(query)
    if top_link:
        print(top_link)
    else:
        print("No results found.")

# Run the async main function
asyncio.run(main())
