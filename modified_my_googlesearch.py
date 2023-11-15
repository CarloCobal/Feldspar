
import requests
import sys
sys.path.append('Ai')
from simpleChat import general_api_call, refinedFilter, parse_questions  # Importing the necessary functions from simpleChat.py
from imgGen import imgGen

def google_custom_search(query):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": 'AIzaSyDVpsjiR3aW_GjgmkT7JYuPpbV_9oeH8zo',
        "cx": '6364b30a9a55746b1',
        "q": query
    }
    response = requests.get(url, params=params)
    return response.json()

def perform_searches(user_input):
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
        # print(f"Question {key}:", question)  # Debugging

        if question:
            results = google_custom_search(question)
            # print("Google search results:", results)  # Debugging

            if 'items' in results and len(results['items']) > 0:
                first_result = results['items'][0]
                title = first_result.get('title', 'No title')
                link = first_result.get('link', 'No URL')
                search_results.append({'title': title, 'url': link})
            else:
                search_results.append({'title': 'No results found', 'url': ''})

    return search_results

#Either save title for something down the line or simplify and save in format that will be used in updating the html, right it is needless extra unless there's a use for that elsewhere.
def imgGenUnrefinedOutput(search_results):
    output_lines = []  # List to collect output lines
    for result in search_results:
        title = result['title']
        img_url = imgGen(title)
        output_line = f"Generated image for '{title}': {img_url}"
        output_lines.append(output_line)
    return '\n'.join(output_lines)  # Combine all lines into one output string

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

if __name__ == "__main__":
    # Example usage with user input
    user_input = "Your user input here"  # Replace with the actual user input
    search_results = perform_searches("hello world")#replace with user_input upon final
    print(parse_image_urls(imgGenUnrefinedOutput(search_results)))

#new output:
"""{'image_1': 'https://oaidalleapiprodscus.blob.core.windows.net/private/org-4OAtU4w8Dcrgyv6hS6wAoI0b/user-ccvP6GnVd9tifqkHAaGiiW2L/img-VuLRwsglzxkjFDZ8UtTZttNJ.png?st=2023-11-15T22%3A54%3A22Z&se=2023-11-16T00%3A54%3A22Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-11-15T23%3A52%3A52Z&ske=2023-11-16T23%3A52%3A52Z&sks=b&skv=2021-08-06&sig=zPrfH5HRhZo%2ByxxzSyE34uWABzLpfK0BaxWt/QbIhn0%3D', 
'image_2': 'https://oaidalleapiprodscus.blob.core.windows.net/private/org-4OAtU4w8Dcrgyv6hS6wAoI0b/user-ccvP6GnVd9tifqkHAaGiiW2L/img-jm3CBQtMV08gYD87CFNCwYyA.png?st=2023-11-15T22%3A54%3A31Z&se=2023-11-16T00%3A54%3A31Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-11-15T23%3A54%3A15Z&ske=2023-11-16T23%3A54%3A15Z&sks=b&skv=2021-08-06&sig=ALco5ehgl5kyoWXQGBzbEjUKhcSWFvWN57uyc800GLQ%3D', 
'image_3': 'https://oaidalleapiprodscus.blob.core.windows.net/private/org-4OAtU4w8Dcrgyv6hS6wAoI0b/user-ccvP6GnVd9tifqkHAaGiiW2L/img-EBIhAOBg58M9ZZFSHMJVKQZg.png?st=2023-11-15T22%3A54%3A39Z&se=2023-11-16T00%3A54%3A39Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-11-15T23%3A54%3A39Z&ske=2023-11-16T23%3A54%3A39Z&sks=b&skv=2021-08-06&sig=ll3eWb%2BhYy1vDEe7quhyT5hWOcVUQH9W94KyyxpRZbw%3D'}"""
   
   
#old output with title:
    "<class 'list'>"
"""[{'title': 'How to Find the Most Accurate Weather Forecasting App', 'url': 'https://time.com/6291479/most-accurate-weather-forecast-apps-2023/'}, 
{'title': 'Weather Underground: Local Weather Forecast, News and Conditions', 'url': 'https://www.wunderground.com/'}, 
{'title': 'Outdoor Thermometers - Weather Stations - The Home Depot', 'url': 'https://www.homedepot.com/b/Outdoors-Garden-Center-Outdoor-Decor-Weather-Stations-Outdoor-Thermometers/N-5yc1vZcl26'}]"""