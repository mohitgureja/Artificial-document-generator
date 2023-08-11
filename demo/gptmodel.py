import os

import openai

from data_generator import helper

openai.api_key = os.getenv("OPENAI_API_KEY")

RESPONSE_FILE_PATH = "data/input/renderer/gpt_response.json"
query = "Generate 10 sentences similar to \"Für ärztliche Leistungen erlauben wir uns, Ihnen\t28,78 EUR\tzu berechnen.\" but instead of amount 28,78 use <amount> tag"

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": query
        },
    ],
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)
print(response)
helper.write_json(response, RESPONSE_FILE_PATH)
