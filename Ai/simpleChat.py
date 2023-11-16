#This outputs a dict of three quesitons to be searched with google.
import openai
import sys

openai.api_key = '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'

"""Question one"""
def general_api_call(user_prompt):
    """Finds the best version of something based on a user prompt"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            # "please suggest the best versions or examples of based on the user response. Please only answer in a 1-3 format no labels or other information is needed."#alt to test later"
            {'role': 'system', 'content': "Please make three suggestions 1 to 3, based on the user prompt ranging from what they ought to know (through consensus) to what they want to know. Keep it short and simple. No need to label with consensus or practical information etc."},# This is because three options is simple and it empowers users to have the option to choose productivity through leisure."},

            {'role': 'user', 'content': user_prompt}
        ],
        max_tokens=150
    )
    return response['choices'][0]['message']['content']
"""output format (probably variable):
1. Learn programming languages like Python or Java to understand 'Hello World', which is traditionally the first program you write when learning a new coding language. 
2. Try various coding platforms or integrated development environments (IDEs) like Codecademy, Repl.it, or PyCharm to practice coding. 
3. Explore courses on coding basics and algorithmic thinking to expand your technical skillset.
"""

"Question two"
def refinedFilter(user_prompt):
    """Parses last answer and translates it into a google search, consider --through tests-- doing this in one go from the start."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {'role': 'system', 'content': "Given the following text, please find three searchable questions that I can ask google. No other text is needed. Label these 1 through 3."},
            {'role': 'user', 'content': user_prompt}
        ],
        max_tokens=150
    )
    return response['choices'][0]['message']['content']

def parse_questions(refined_response):
    """
    Parses the output string to extract questions and stores them in a dictionary.
    Each question is associated with a key representing its sequence.
    """
    # Split the output string into lines
    questions = {}
    for line in refined_response.split('\n'):
        try:
            label, question = line.split('. ', 1)
            questions[label.strip()] = question.strip()
        except ValueError:
            # Handle lines that don't have the expected format
            print(f"Skipping line due to unexpected format: {line}")
            continue
    return questions

# Example usage
output = """
1. What are the various functions and features of an online platform?
2. How can I seek assistance from an online community?
3. How can updating settings/preferences enhance user experience on a platform?
"""
# questions_dict = parse_questions(output) #outputs:
"""{'Q1': 'What are the various functions and features of an online platform?', 'Q2': 'How can I seek assistance from an online community?', 'Q3': 'How can updating settings/preferences enhance user experience on a platform?'}"""

if __name__ == "__main__":
    user_input = sys.argv[1] if len(sys.argv) > 1 else "Default User Input"
    parse_questions(refinedFilter(general_api_call(user_input)))