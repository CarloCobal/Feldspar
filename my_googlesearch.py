import requests
import sys
import json

def google_custom_search(query):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": 'AIzaSyDVpsjiR3aW_GjgmkT7JYuPpbV_9oeH8zo',
        "cx": '6364b30a9a55746b1',
        "q": query
    }
    response = requests.get(url, params=params)
    return response.json()

# Replace 'YOUR_API_KEY' and 'YOUR_CSE_ID' with your actual API Key and Custom Search Engine ID
# query = "Healdsburg history"

# results = google_custom_search(query)

#Returns all results from a query.
# for item in results.get('items', []):
#     title = item.get('title')
#     link = item.get('link')
#     print(f"Title: {title}\nLink: {link}\n")

#returns just the top result of a query
if __name__ == "__main__":
    user_query = sys.argv[1] if len(sys.argv) > 1 else "Default Query"
    results = google_custom_search(user_query)

    # Extracting the first search result link
    top_result_link = results['items'][0]['link'] if results.get('items') else None
    print(json.dumps({"top_link": top_result_link}))