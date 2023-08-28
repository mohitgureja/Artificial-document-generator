import os

import openai

from components.data_generator import helper

openai.api_key = os.getenv("OPENAI_API_KEY")
RESPONSE_FILE_PATH = "data/input/renderer/gpt_response.json"


def get_pairs_content(key, content: list, isKeyPair: bool):
    """
    :param key: str
    :param content: list
    :type isKeyPair: bool
    """
    data = {}
    if isKeyPair:
        data[key] = [text.split(':') for text in content]
    else:
        data[key] = content
    return data


def generate_gpt_sentence(key, query, isKeyPair):
    """
    Generate g
    :param isKeyPair:
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
    content = content.split("\n")
    data = get_pairs_content(key, content, isKeyPair)
    helper.write_json(data, RESPONSE_FILE_PATH)
    return data[key]
