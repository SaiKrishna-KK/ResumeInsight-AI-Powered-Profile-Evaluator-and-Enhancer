import os
import openai
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "who are you?"}
    ],
    max_tokens=256,
    temperature=0.7,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)

print(response.choices[0].message['content'])
