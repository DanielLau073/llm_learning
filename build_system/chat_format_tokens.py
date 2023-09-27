'''
语言模型，提问范式与 Token
对于英文输入，一个 token 一般对应 4 个字符或者四分之三个单词；对于中文输入，一个 token 一般对应一个或半个词。不同模型有不同的 token 限制，需要注意的是，这里的 token 限制是输入的 Prompt 和输出的 completion 的 token 数之和，因此输入的 Prompt 越长，能输出的 completion 的上限就越低。 ChatGPT3.5-turbo 的 token 上限是 4096。
'''
import os
import openai
import tiktoken

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]

## Tokens
# response = get_completion("Take the letters in lollipop and reverse them")
# response = get_completion("""Take the letters in l-o-l-l-i-p-o-p and reverse them""")
# print(response)

## Helper function (chat format)
# def get_completion_from_messages(messages, 
#                                  model="gpt-3.5-turbo", 
#                                  temperature=0, 
#                                  max_tokens=500):
#     response = openai.ChatCompletion.create(
#         model=model,
#         messages=messages,
#         temperature=temperature, # this is the degree of randomness of the model's output
#         max_tokens=max_tokens, # the maximum number of tokens the model can ouptut 
#     )
#     return response.choices[0].message["content"]

def get_completion_and_token_count(messages,
                                   model="gpt-3.5-turbo",
                                   temperature=0,
                                   max_tokens=500):

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    content = response.choices[0].message["content"]

    token_dict = {
'prompt_tokens':response['usage']['prompt_tokens'],
'completion_tokens':response['usage']['completion_tokens'],
'total_tokens':response['usage']['total_tokens'],
    }

    return content, token_dict

messages =  [  
{'role':'system',
 'content':"""You are an assistant who \
responds in the style of Dr Seuss."""},    
{'role':'user',
 'content':"""write me a story about a happy carrot"""},
] 
response, token_dict = get_completion_and_token_count(messages,temperature =1)
print(response)
print(token_dict)
