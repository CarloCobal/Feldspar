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

#returns just the top result of a query
if __name__ == "__main__":
    user_query = sys.argv[1] if len(sys.argv) > 1 else "Default Query"
    results = google_custom_search(user_query)
    print(results)

    # Extracting the first search result link
    top_result_link = results['items'][0]['link'] if results.get('items') else None
    # json.dumps({"top_link": top_result_link})
    print(json.dumps({"top_link": top_result_link}))



# async def google_custom_search(query):
#     url = "https://www.googleapis.com/customsearch/v1"
#     params = {
#         # "key": 'AIzaSyDVpsjiR3aW_GjgmkT7JYuPpbV_9oeH8zo',
#         "key": 'AIzaSyCqrnzM-GLKIZalq_AmA3uvpuchiZJZQLQ',
#         "cx": '94eb91fc4b7e143e4',
#         "q": query
#     }