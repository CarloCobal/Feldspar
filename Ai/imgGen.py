
import openai
import sys
import json

openai.api_key = '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'

def imgGen(imgPrompt):
    fullPrompt = imgPrompt + " Please make the art's theme a matte color scheme. Something simple yet beautiful. Can you shoot it like a movie film with a black cropped top and bottom?"
    response = openai.Image.create(
        prompt=fullPrompt,
        n=1,
        size="1024x1024"
    )
    # Extracting the URL from the response and printing it as JSON
    img_url = response['data'][0]['url']
    return img_url
    # print(json.dumps({"url": img_url}))

# if __name__ == "__main__":
#     user_prompt = sys.argv[1] if len(sys.argv) > 1 else "Default Prompt"
#     response = imgGen(user_prompt)
#     if response:
#         print(json.dumps({"url": response['data'][0]['url']}))  # Only print the JSON


#use as imgGen(input()) and specify what the img is through the url req
