from ollama import chat
from ollama import ChatResponse

# response: ChatResponse = chat(model='deepseek-r1:1.5b', messages=[
#   {
#     'role': 'user',
#     'content': 'Explain the bellman optimality principle',
#   },
# ])
# print(response['message']['content'])
# # or access fields directly from the response object
# print(response.message.content)

import re

def ask_deepseek(input_content, system_prompt, deep_think = True, print_log = True):
    response: ChatResponse = chat(model='deepseek-r1:8b', messages=[
        {'role' : 'system', 'content' : system_prompt},
        {'role': 'user','content': input_content}
    ])
    response_text = response['message']['content']
    if print_log: print(response_text)

    # Use a regular expression to extract all of the deep think text
    think_texts = re.findall(r'<think>(.*?)</think>', response_text, flags=re.DOTALL)

    # Join extracted think sections, if multiple exist
    think_texts = "/n/n".join(think_texts).strip()

    # Exclude the deep think and just return the response
    clean_response= re.sub(r'<think>.*?</think', '', response_text, flags=re.DOTALL).strip()

    # Return the response only, or the response and the think text as a tuple.
    return clean_response if not deep_think else (clean_response, think_texts)


# prompt = "Dear temple workers and friends We have two announcements that we would like to share with you First attached is a PDF on How to Find the Temple Worker Portal and Get a Substitute We hope this will be a helpful tool for you Second we wanted to take the opportunity to introduce the members of the new temple leadership – the presidency matron and assistants to the matron – who will begin leading the Provo City Center Temple on September 1st Please enjoy learning a bit about them and join us in welcoming them Thank you for all you do brothers and sisters We are grateful for you Ken Craig Temple Recorder Provo City Center Utah Temple The Church of Jesus Christ of Latterday Saints Mobile 801 493 9410 Email kencraig@churchofjesuschristorg"

# memory = "You are an email assistant. You look at emails that arrive in my inbox, and reply to them if they require a response. To be clear, the prompts I am giving you are emails from my inbox. If they do not seem like they require a response, simply respond with NULL. You may come accross questions in these emails that you need more information from me as the user on. If you have any questions about what I might want or prefer, simply respond with a json object in the form of {type: email, question: <your question goes here>}. Otherwise, respond on my behalf."

# response, think = ask_deepseek(prompt, memory, print_log=False)

# print("Response")
# print(response)

# print()

# print("Thinking")
# print(think)