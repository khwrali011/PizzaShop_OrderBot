import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_type = os.getenv("api_type")
openai.api_base = os.getenv("api_base")
openai.api_version = os.getenv("api_version")
openai.api_key = os.getenv("OPENAI_API_KEY")
engine=os.getenv("engine")

class ResponseGenerator:
    def __init__(self):
        self.model = "gpt-3.5-turbo-16k"
        self.max_tokens = 10000

    def generate_response(self, messages):

        completion = openai.ChatCompletion.create(
            engine=engine,
            messages=messages,
            temperature=0.1)
        
        return completion.choices[0].message["content"]
