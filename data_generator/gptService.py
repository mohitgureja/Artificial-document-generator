import os

import openai

from data_generator import helper

openai.api_key = os.getenv("OPENAI_API_KEY")
RESPONSE_FILE_PATH = "data/input/renderer/gpt_response.json"


def generate_gpt_sentence(key, query):
    """
    Generate g
    :param query:
    :return: [String]
    """
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

    content = response["choices"][0]["message"]["content"]
    data = {key, content}
    helper.write_json(data, RESPONSE_FILE_PATH)
    return content.split("\n")
