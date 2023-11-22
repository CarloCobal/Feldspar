# import google.generativeai as palm
import requests
# palm.configure(api_key='AIzaSyDvnKzhAEh5EnrYoy7wvS1_MMcD3pcRG6M')

# Set your API key
api_key = 'AIzaSyDvnKzhAEh5EnrYoy7wvS1_MMcD3pcRG6M'

# Set the API URL
url = "https://generativelanguage.googleapis.com/v1beta3/models/text-bison-001:generateText"

# Set the headers
headers = {
    "Content-Type": "application/json",
    "x-goog-api-key": api_key
}

# Set the data payload
data = {
    "prompt": {"text": "Give me five subcategories of jazz"}
}

# Make the POST request
response = requests.post(url, json=data, headers=headers)

# Print the response
# print(response.json())
json_response = response.json()

# Extract and print the 'output' portion
if 'candidates' in json_response and json_response['candidates']:
    output = json_response['candidates'][0]['output']
    print(output)
else:
    print("No output found in the response.")

# # Create a new conversation
# response = palm.chat(messages='Hello')

# # Last contains the model's response:
# print(response.last)

# # Add to the existing conversation by sending a reply
# response = response.reply("Just chillin'")
# # See the model's latest response in the `last` field:
# print(response.last)
# print(response.messages)

# reply = palm.chat(context="Speak like Shakespeare.", messages='Hello')
# print(reply.last)

# to run
# /opt/homebrew/bin/python3 /Users/quaidbulloch/Documents/Code/Feldspar/NewFeldspar/Ai/palm.py