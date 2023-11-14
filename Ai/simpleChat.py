import openai
import sys

openai.api_key = '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'


"""Finds the best version of something based on a user prompt"""
# sys_prompt = 'Please find me the best. I will provide you with a word or phrase then I want you to find the "best versions or possible examples of" that word or phrase. These could be historical examples, or critially acclaimed things. I just want to see the best of what ever it is that I am about to provide. Please do not provide extended descriptions for why they might be the best. I just want to know what it is please.'
#"please suggest appropriate ways to view or engage with this media: E.g. Expedia for travel suggestions, Youtube for cool things to see. Netflix for great shows to watch, nature for great interesting articles to read etc. The result should be relevant to the input of what is the best."
def general_api_call(user_prompt):#, system_prompt='Hi how are you?'):
    # Make the API call
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            # {'role': 'system', 'content': """Please find me three of the best. I will provide you with a word or phrase then I want you to find the "best versions or possible examples of" that word or phrase. These could be historical examples, or critially acclaimed things. I just want to see the best of what ever it is that I am about to provide. Please do not provide extended descriptions for why they might be the best. I just want to know what it is please. Based on those three, please suggest appropriate ways to view or engage with this media: E.g. Expedia for travel suggestions, Youtube for cool things to see. Netflix for great shows to watch, nature for great interesting articles to read etc. The result should be relevant to the input of what is the best. The answer should be in order and a single word. There may be duplicates for the medium of experience, e.g. two instances of netflix etc. One more thing. Make a judgement call of what is best for a user on the basis of productive to leisurely. Sort of assuming the genre for them. E.g. for movies it would range from cognitive thriller to low stakes rom com. Or for travel it would range by distance. E.g. it should range from the amount of effort needed to exert. A. Long distance like another country. B. Short domestic distance. C. Local destinations/activities. Please only use letters for this listing. You have the option to return a one word request like location that the user may input if necessary, depending on the situation. Could do something like: Movies; A. What is a movie, how are they made. (something cognitively difficult and related to learning. B. local cinemas playing movie x if it was in the prompt. C. A great show on an at home media player related to their query. Please make those suggestions one word and the website associated with that one word."""},
            {'role': 'system', 'content': "Please make three suggestions 1 to 3, based on the user prompt ranging from what they ought to know (through consensus) to what they want to know. Keep it short and simple. No need to label with consensus or practical information etc."},# This is because three options is simple and it empowers users to have the option to choose productivity through leisure."},

            {'role': 'user', 'content': user_prompt}
        ],
        max_tokens=150
    )
    return response['choices'][0]['message']['content']

# prompt = "OpenAi Platform"
# print(prompt, general_api_call(prompt))

if __name__ == "__main__":
    user_input = sys.argv[1] if len(sys.argv) > 1 else "Default User Input"
    # system_input = sys.argv[2] if len(sys.argv) > 2 else "Default System Input"
    print(general_api_call(user_input))
#now look them up.
#Also, order based on what is most productive to least productive. 
#   options, I can do so based off of multiple search queries. (Blanket statement that this isn't useful but may test with users.)
    #   I can make a judgement call of what is best for a user on the basis of productive to leisurely. Sort of assuming the genre for them. E.g. for movies it would range from cognative thriller to low stakes rom com. Or for travel it would range by distance. E.g. it should range from the amount of effort needed to exert. A. Long distance like another country. B. Short domestic distance. C. Local destinations/activities.
#How can I abstract that?

#didn't work with the movie prompt. Could do something like: Movies; A. What is a movie, how are they made. (something cognitively difficult and related to learning. B. local cinemas playing movie x if it was in the prompt. C. A great show on an at home media player related to their query. 

#LeftLink, Middlelink, RightLink: Feldspar.