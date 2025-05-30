
import os
from dotenv import load_dotenv
from openai import OpenAI


def load_env():
    load_dotenv(override=True)
    api_key = os.getenv('OPENAI_API_KEY')

    # Check the key
    if not api_key:
        print("No API key was found")
    elif not api_key.startswith("sk-proj-"):
        print("An API key was found, but it doesn't start sk-proj-")
    elif api_key.strip() != api_key:
        print("An API key was found, but it looks like it might have space or tab characters at the start or end - please remove them - see troubleshooting notebook")
    else:
        print("OpenAPI!")
    return api_key


# // singleton pattern
openaiInstance = None
def load_open_ai():
    global openaiInstance
    if not openaiInstance:
        openaiInstance = OpenAI(api_key=load_env())
    return openaiInstance