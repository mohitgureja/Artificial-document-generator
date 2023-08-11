from data_generator import helper

# GPT_RESPONSE_FILE_PATH = "data/input/renderer/gpt_response.json"
GPT_RESPONSE_FILE_PATH = "/Users/ssdn/PycharmProjects/Artificial-document-generator/data/input/renderer/gpt_response.json"

gpt_response = helper.read_json(GPT_RESPONSE_FILE_PATH)
key = "product_name"
isKeyPair = True
content = gpt_response[key].split("\n")
data = {}
if isKeyPair:
    data[key] = [text.split(':') for text in content]
else:
    data[key] = content

print(data[key])
# firstword, secondword= data[key].split(' ', 1)
#
#
# pattern = r'^[a-zA-ZäüöẞÖÜÄ]+$'
# if not re.match(pattern, firstword):
#     print(secondword)
# else:
#     print(firstword)
