import re
from ollama import chat, ChatResponse

def ask_deepseek(input_content: str, system_prompt: str, deep_think: bool = True, print_log: bool = True):
    """
    Sends a message to the DeepSeek model via Ollama and returns the response.

    Args:
        input_content (str): The main message (e.g. an email).
        system_prompt (str): The system prompt to condition the model's behavior.
        deep_think (bool): Whether to return <think> content separately.
        print_log (bool): Whether to print the raw model output.

    Returns:
        str | Tuple[str, str]: Cleaned response (and extracted <think> section if deep_think=True).
    """
    response: ChatResponse = chat(
        model='deepseek-r1:8b',
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': input_content}
        ]
    )
    
    response_text = response['message']['content']
    if print_log:
        print(response_text)

    # Extract all <think> sections
    think_sections = re.findall(r'<think>(.*?)</think>', response_text, flags=re.DOTALL)
    combined_thoughts = "\n\n".join(think_sections).strip()

    # Clean the response by removing all <think> blocks
    clean_response = re.sub(r'<think>.*?</think>', '', response_text, flags=re.DOTALL).strip()

    return (clean_response, combined_thoughts) if deep_think else clean_response
