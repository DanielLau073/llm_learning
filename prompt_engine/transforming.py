'''
文本转换
How to use Large Language Models for text transformation tasks such as language translation, spelling and grammar checking, tone adjustment, and format conversion.
'''
import openai
import os
import time
from redlines import Redlines
from IPython.display import display, Markdown
#from IPython.display import display, Markdown, Latex, HTML, JSON

# from dotenv import load_dotenv, find_dotenv
# 读取本地/项目的环境变量。

def get_openai_key():
    # find_dotenv()寻找并定位.env文件的路径
    # load_dotenv()读取该.env文件，并将其中的环境变量加载到当前的运行环境中  
    # 如果你设置的是全局的环境变量，这行代码则没有任何作用。
    ##_ = load_dotenv(find_dotenv())
    return os.environ['OPENAI_API_KEY']

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

openai.api_key = get_openai_key()

## Translation
# prompt = f"""
# Translate the following English text to Spanish: \
# ```Hi, I would like to order a blender```
# """
# prompt = f"""
# Tell me which language this is:
# ```Combien coûte le lampadaire?```
# """
# prompt = f"""
# Translate the following  text to French and Spanish
# and English pirate: \
# ```I want to order a basketball```
# """
# prompt = f"""
# Translate the following text to Spanish in both the \
# formal and informal forms:
# 'Would you like to order a pillow?'
# """

### Universal Translator
# user_messages = [
#   "La performance du système est plus lente que d'habitude.",  # System performance is slower than normal         
#   "Mi monitor tiene píxeles que no se iluminan.",              # My monitor has pixels that are not lighting
#   "Il mio mouse non funziona",                                 # My mouse is not working
#   "Mój klawisz Ctrl jest zepsuty",                             # My keyboard has a broken control key
#   "我的屏幕在闪烁"                                             # My screen is flashing
# ] 
# for issue in user_messages:
#     prompt = f"Tell me what language this is: ```{issue}```"
#     lang = get_completion(prompt)
#     print(f"Original message ({lang}): {issue}")
# 
#     prompt = f"""
#     Translate the following  text to English \
#     and Korean: ```{issue}```
#     """
#     response = get_completion(prompt)
#     print(response, "\n")
# 

## Tone Transformation
# prompt = f"""
# Translate the following from slang to a business letter:
# 'Dude, This is Joe, check out this spec on this standing lamp.'
# """

## Format Conversion
# data_json = { "resturant employees" :[ 
#     {"name":"Shyam", "email":"shyamjaiswal@gmail.com"},
#     {"name":"Bob", "email":"bob32@gmail.com"},
#     {"name":"Jai", "email":"jai87@gmail.com"}
# ]}
# prompt = f"""
# Translate the following python dictionary from JSON to an HTML \
# table with column headers and title: {data_json}
# """
 
## Spellcheck/Grammar check.
# text = [ 
#   "The girl with the black and white puppies have a ball.",  # The girl has a ball.
#   "Yolanda has her notebook.", # ok
#   "Its going to be a long day. Does the car need it’s oil changed?",  # Homonyms
#   "Their goes my freedom. There going to bring they’re suitcases.",  # Homonyms
#   "Your going to need you’re notebook.",  # Homonyms
#   "That medicine effects my ability to sleep. Have you heard of the butterfly affect?", # Homonyms
#   "This phrase is to cherck chatGPT for speling abilitty"  # spelling
# ]
# for t in text:
#     prompt = f"""Proofread and correct the following text
#     and rewrite the corrected version. If you don't find
#     and errors, just say "No errors found". Don't use 
#     any punctuation around the text:
#     ```{t}```"""
#     response = get_completion(prompt)
#     print(response)

text = f"""
Got this for my daughter for her birthday cuz she keeps taking \
mine from my room.  Yes, adults also like pandas too.  She takes \
it everywhere with her, and it's super soft and cute.  One of the \
ears is a bit lower than the other, and I don't think that was \
designed to be asymmetrical. It's a bit small for what I paid for it \
though. I think there might be other options that are bigger for \
the same price.  It arrived a day earlier than expected, so I got \
to play with it myself before I gave it to my daughter.
"""
#prompt = f"proofread and correct this review: ```{text}```"



prompt = f"""
proofread and correct this review. Make it more compelling.
Ensure it follows APA style guide and targets an advanced reader.
Output in markdown format.
Text: ```{text}```
"""
response = get_completion(prompt)
display(Markdown(response))
print(prompt)
print(response)


# diff = Redlines(text,response)
# display(Markdown(diff.output_markdown))
# 
#display(HTML(response)) 



