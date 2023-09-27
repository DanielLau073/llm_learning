'''
文本扩展
generate customer service emails that are tailored to each customer's review.
'''
import openai
import os
import time

# from dotenv import load_dotenv, find_dotenv
# 读取本地/项目的环境变量。

def get_openai_key():
    # find_dotenv()寻找并定位.env文件的路径
    # load_dotenv()读取该.env文件，并将其中的环境变量加载到当前的运行环境中  
    # 如果你设置的是全局的环境变量，这行代码则没有任何作用。
    ##_ = load_dotenv(find_dotenv())
    return os.environ['OPENAI_API_KEY']

def get_completion(prompt, model="gpt-3.5-turbo", temperature=1.0): # 添加 temperature 参数，并设置默认值为 1.0
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # 使用传递进来的 temperature 值
    )
    return response.choices[0].message["content"]

openai.api_key = get_openai_key()

# given the sentiment from the lesson on "inferring",
# and the original customer message, customize the email
sentiment = "negative"

# review for a blender
review = f"""
So, they still had the 17 piece system on seasonal \
sale for around $49 in the month of November, about \
half off, but for some reason (call it price gouging) \
around the second week of December the prices all went \
up to about anywhere from between $70-$89 for the same \
system. And the 11 piece system went up around $10 or \
so in price also from the earlier sale price of $29. \
So it looks okay, but if you look at the base, the part \
where the blade locks into place doesn’t look as good \
as in previous editions from a few years ago, but I \
plan to be very gentle with it (example, I crush \
very hard items like beans, ice, rice, etc. in the \
blender first then pulverize them in the serving size \
I want in the blender then switch to the whipping \
blade for a finer flour, and use the cross cutting blade \
first when making smoothies, then use the flat blade \
if I need them finer/less pulpy). Special tip when making \
smoothies, finely cut and freeze the fruits and \
vegetables (if using spinach-lightly stew soften the \
spinach then freeze until ready for use-and if making \
sorbet, use a small to medium sized food processor) \
that you plan to use that way you can avoid adding so \
much ice if at all-when making your smoothie. \
After about a year, the motor was making a funny noise. \
I called customer service but the warranty expired \
already, so I had to buy another one. FYI: The overall \
quality has gone done in these types of products, so \
they are kind of counting on brand recognition and \
consumer loyalty to maintain sales. Got it in about \
two days.
"""

## Remind the model to use details from the customer's email
# prompt = f"""
# You are a customer service AI assistant.
# Your task is to send an email reply to a valued customer.
# Given the customer email delimited by ```, \
# Generate a reply to thank the customer for their review.
# If the sentiment is positive or neutral, thank them for \
# their review.
# If the sentiment is negative, apologize and suggest that \
# they can reach out to customer service. 
# Make sure to use specific details from the review.
# Write in a concise and professional tone.
# Sign the email as `AI customer agent`.
# Customer review: ```{review}```
# Review sentiment: {sentiment}
# """

## Remind the model to use details from the customer's email
prompt = f"""
You are a customer service AI assistant.
Your task is to send an email reply to a valued customer.
Given the customer email delimited by ```, \
Generate a reply to thank the customer for their review.
If the sentiment is positive or neutral, thank them for \
their review.
If the sentiment is negative, apologize and suggest that \
they can reach out to customer service.
Make sure to use specific details from the review.
Write in a concise and professional tone.
Sign the email as `AI customer agent`.
Customer review: ```{review}```
Review sentiment: {sentiment}
"""
print(prompt)
# response = get_completion(prompt)
response = get_completion(prompt, temperature=0.7)
print(response)

