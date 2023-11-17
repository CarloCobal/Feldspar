#This outputs a dict of three quesitons to be searched with google.
# A* "please suggest the best versions or examples of based on the user response. Please only answer in a 1-3 format no labels or other information is needed."#alt to test later" # This is because three options is simple and it empowers users to have the option to choose productivity through leisure."},
import openai
import sys
import asyncio
from toplink import google_custom_search  # Importing from toplink.py

openai.api_key = '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'

"""Question one"""
def call1(user_prompt, intake):
    """Finds the best version of something based on a user prompt"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {'role': 'system', 'content': intake},#A* 

            {'role': 'user', 'content': user_prompt}
        ],
        max_tokens=150
    )
    return response['choices'][0]['message']['content']


# user_input = "top ten tech startups"
user_input = "What is an llm?"

print(user_input)

# question1 = "Please find me the best possible examples of:"
question1=""
# print(call1(user_input, question1))

question2= "Given the following text, please find three relevant searchable questions that I can ask google. No other text is needed. Label these 1 through 3."
# print(call1(call1(user_input, question1), question2))

question3= f"can you please determine if {user_input} should be searched directly with google, or if it doesn't seem like something that needs an immediate or updated information can you please answer it with chat? The answer should be one word to determine if it will go through the chat loop or an immediate google search: 1. chat, 2. google."
print(call1(call1(call1(user_input, question1), question2), question3))

#sometimes outputs one word rec.

#q3 determines what gets displayed. If it says chat for all three then lookup based on that. Otherwise do a direct google search and directly lookup that portion of the output?
#wait what happens if it outputs chat? There is no chat interface. 


#lets call it further discovery instead of chat and feed it through.

async def process_output(output, action):
    while action == "chat":
        # Modify the prompt to refine the output into a searchable query
        modified_prompt = f"Refine this query: {output}"
        output = call1(modified_prompt, question1)  # Adjust the question as needed
        action = call1(output, question3)  # Check if it's ready for Google search

    if action == "google":
        top_link = await google_custom_search(output)
        print(f"Search result for '{output}': {top_link}")

async def main():
    user_input = "Your initial user input"
    question2_outputs = call1(call1(user_input, question1), question2).split("\n")
    question3_decisions = call1(user_input, question3).split("\n")

    for q2_output, decision in zip(question2_outputs, question3_decisions):
        await process_output(q2_output.strip(), decision.strip().lower())

# Run the async main function
asyncio.run(main())

        #Thinking For You:
#immediately search the one who's output is associated with google. (fix search to be simple top link output).
#other -> continue the dialogue until it becomes something that can be immediately searched with google.