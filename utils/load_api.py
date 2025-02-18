import os
from dotenv import load_dotenv
import aisuite as ai



load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

client = ai.Client()
# models = ["openai:gpt-4o", "anthropic:claude-3-5-sonnet-20240620"]
models =["openai:gpt-4o", "openai:gpt-3.5-turbo-0125"]
messages = [
    {"role": "system", "content": "Respond in Pirate English."},
    {"role": "user", "content": "Tell me a joke."},
]

for model in models:
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.75
    )
    print(response.choices[0].message.content)