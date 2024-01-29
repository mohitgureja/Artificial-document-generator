import ast
import os

import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def process_instance(content, data, key):
    if isinstance(content, dict):
        data.update(content)
    else:
        data[key] = content
    return data


def get_instance(content):
    type = str
    if isinstance(content, dict):
        type = dict
    elif isinstance(content, list):
        type = list
    return type


def generate_gpt_data(data, key, query, output_format):
    """
    Generate gpt sentences for each key
    :param isKeyPair:
    :param query:
    :return: [String]
    """
    query += "\nPlease give response in this output format: " + str(output_format)
    content = call_gpt(query)

    count = 0
    while not get_instance(output_format) == get_instance(content):
        print("GPT response is not in desired output format. Trying again!")
        if count > 5:
            break
        content = call_gpt(query)
        count += 1
    content = process_instance(content, data, key)
    return content


def call_gpt(query):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": query
            },
        ],
        temperature=1,
        max_tokens=3072,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    content = response["choices"][0]["message"]["content"]
    print(content)
    try:
        content = ast.literal_eval(content)
    except SyntaxError:
        print("GPT response is in string format.")
    return content
