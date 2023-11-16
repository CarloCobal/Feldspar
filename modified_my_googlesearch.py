
import aiohttp
import asyncio
import requests
import json
import sys

sys.path.append('Ai')
from simpleChat import general_api_call, refinedFilter, parse_questions  # Importing the necessary functions from simpleChat.py
# from imgGen import imgGen
from imgGen import imgGenUnrefinedOutput, async_imgGen

async def google_custom_search(query):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        # "key": 'AIzaSyDVpsjiR3aW_GjgmkT7JYuPpbV_9oeH8zo',
        "key": 'AIzaSyCqrnzM-GLKIZalq_AmA3uvpuchiZJZQLQ',
        "cx": '94eb91fc4b7e143e4',
        "q": query
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            return await response.json()

async def perform_searches(user_input):
    # Call the general_api_call function and process its output
    chat_response = general_api_call(user_input)
    # print("Chat response:", chat_response)  # Debugging

    refined_response = refinedFilter(chat_response)
    # print("Refined response:", refined_response)  # Debugging

    questions = parse_questions(refined_response)
    # print("Questions:", questions)  # Debugging
    
    search_results = []
    for key in ['1', '2', '3']:
        question = questions.get(key)
        if question:
            results = await google_custom_search(question)
            # print("Google search results:", results)  # Debugging

            if 'items' in results and len(results['items']) > 0:
                for item in results['items']:
                    title = item.get('title', 'No title')
                    link = item.get('link', 'No URL')
                    # Add both title and link to the search_results
                    search_results.append({'title': title, 'url': link})
            else:
                search_results.append({'title': 'No results found', 'url': ''})
        # print(search_results)
    return search_results

#Either save title for something down the line or simplify and save in format that will be used in updating the html, right it is needless extra unless there's a use for that elsewhere.
async def imgGenUnrefinedOutput(search_results):
    output_results = []
    for result in search_results[:3]:  # Limit to first three results
        try:
            img_url = await async_imgGen(result['title'])
        except Exception as e:
            print(f"Error generating image for '{result['title']}': {e}", file=sys.stderr)
            img_url = "default_image_url"
        result['img_url'] = img_url  # Add img_url to result
        output_results.append(result)  # Add the entire result dict to output
    return output_results

 # Combine all lines into one output string

        # print(f"Generated image for '{title}': {img_url}")
"""Generated image for 'Here's how AI helps humans make informed decisions | World ...': https://oaidalleapiprodscus.blob.core.windows.net/private/org-4OAtU4w8Dcrgyv6hS6wAoI0b/user-ccvP6GnVd9tifqkHAaGiiW2L/img-YrhUge1XI6MA9MvCCKbj8Chq.png?st=2023-11-15T21%3A30%3A36Z&se=2023-11-15T23%3A30%3A36Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-11-15T22%3A30%3A36Z&ske=2023-11-16T22%3A30%3A36Z&sks=b&skv=2021-08-06&sig=YZQtCccSbbLll4iBCc4rc1DW8JK7w/j168PPXsdn8qw%3D"""

def parse_image_urls(output):
    lines = output.split('\n')  # Split the output into lines
    image_dict = {}
    for i, line in enumerate(lines):
        if 'Generated image for' in line:
            url_start = line.find('http')  # Find the start of the URL
            if url_start != -1:
                url = line[url_start:].strip()  # Extract the URL
                key = f'image_{i + 1}'  # Create a key for the dictionary
                image_dict[key] = url
    return image_dict

async def main():
    # Check if a command-line argument is provided
    if len(sys.argv) > 1:
        user_input = sys.argv[1]  # Use the first command-line argument as input
    else:
        user_input = "default input"  # Default input if no argument is provided

    search_results = await perform_searches(user_input)
    final_output = await imgGenUnrefinedOutput(search_results)
    print(json.dumps(final_output), file=sys.stdout)  # Print final output to stdout

if __name__ == "__main__":
    asyncio.run(main())  # No need to print here, as it's done in main()

