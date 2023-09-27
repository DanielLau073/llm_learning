'''
Chaining Prompts 将复杂任务分解为多个简单Prompt的策略
通过使用链式 Prompt 将复杂任务拆分为一系列简单的子任务。
Chaining Prompts 具有以下优点:
1. 分解复杂度，每个 Prompt 仅处理一个具体子任务，避免过于宽泛的要求，提高成功率。这类似于分阶段烹饪，而不是试图一次完成全部。
2. 降低计算成本。过长的 Prompt 使用更多 tokens ，增加成本。拆分 Prompt 可以避免不必要的计算。
3. 更容易测试和调试。可以逐步分析每个环节的性能。
4. 融入外部工具。不同 Prompt 可以调用 API 、数据库等外部资源。
5. 更灵活的工作流程。根据不同情况可以进行不同操作。
'''

import openai 
from utils.tools import get_completion_from_messages


## 提取产品和类别
delimiter = "####"

system_message = f"""
您将获得客户服务查询。
客户服务查询将使用{delimiter}字符作为分隔符。
请仅输出一个可解析的Python列表，列表每一个元素是一个JSON对象，每个对象具有以下格式：
'category': <包括以下几个类别：Computers and Laptops、Smartphones and Accessories、Televisions and Home Theater Systems、Gaming Consoles and Accessories、Audio Equipment、Cameras and Camcorders>,
以及
'products': <必须是下面的允许产品列表中找到的产品列表>

类别和产品必须在客户服务查询中找到。
如果提到了某个产品，它必须与允许产品列表中的正确类别关联。
如果未找到任何产品或类别，则输出一个空列表。
除了列表外，不要输出其他任何信息！

允许的产品：

Computers and Laptops category:
TechPro Ultrabook
BlueWave Gaming Laptop
PowerLite Convertible
TechPro Desktop
BlueWave Chromebook

Smartphones and Accessories category:
SmartX ProPhone
MobiTech PowerCase
SmartX MiniPhone
MobiTech Wireless Charger
SmartX EarBuds

Televisions and Home Theater Systems category:
CineView 4K TV
SoundMax Home Theater
CineView 8K TV
SoundMax Soundbar
CineView OLED TV

Gaming Consoles and Accessories category:
GameSphere X
ProGamer Controller
GameSphere Y
ProGamer Racing Wheel
GameSphere VR Headset

Audio Equipment category:
AudioPhonic Noise-Canceling Headphones
WaveSound Bluetooth Speaker
AudioPhonic True Wireless Earbuds
WaveSound Soundbar
AudioPhonic Turntable

Cameras and Camcorders category:
FotoSnap DSLR Camera
ActionCam 4K
FotoSnap Mirrorless Camera
ZoomMaster Camcorder
FotoSnap Instant Camera

只输出对象列表，不包含其他内容。
"""

user_message_1 = f"""
 请告诉我关于 smartx pro phone 和 the fotosnap camera 的信息。
 另外，请告诉我关于你们的tvs的情况。 """

messages =  [{'role':'system', 'content': system_message},
             {'role':'user', 'content': f"{delimiter}{user_message_1}{delimiter}"}]
# print(messages)
category_and_product_response_1 = get_completion_from_messages(messages)
# print(category_and_product_response_1)


user_message_2 = f"""我的路由器不工作了"""
messages =  [{'role':'system','content': system_message},
             {'role':'user','content': f"{delimiter}{user_message_2}{delimiter}"}]
# response = get_completion_from_messages(messages)
# print("Test 2")
# print(messages)
# print(response)

## 检索详细信息
# product information
import json
file_path = 'data/products.json'
with open(file_path, 'r') as f:
    products = json.load(f)

def get_product_by_name(name):
    return products.get(name, None)

def get_products_by_category(category):
    return [product for product in products.values() if product["category"] == category]

def generate_output_string(data_list):
    output_string = ""

    if data_list is None:
        return output_string

    for data in data_list:
        try:
            if "products" in data:
                products_list = data["products"]
                for product_name in products_list:
                    product = get_product_by_name(product_name)
                    if product:
                        output_string += json.dumps(product, indent=4) + "\n"
                    else:
                        print(f"Error: Product '{product_name}' not found")
            elif "category" in data:
                category_name = data["category"]
                category_products = get_products_by_category(category_name)
                for product in category_products:
                    output_string += json.dumps(product, indent=4) + "\n"
            else:
                print("Error: Invalid object format")
        except Exception as e:
            print(f"Error: {e}")

    return output_string 

# print(get_product_by_name("TechPro Ultrabook"))
# print("\n\n")
# print(get_products_by_category("Computers and Laptops"))

## 生成查询答案
def read_string_to_list(input_string):
    """
    将输入的字符串转换为 Python 列表。

    参数:
    input_string: 输入的字符串，应为有效的 JSON 格式。

    返回:
    list 或 None: 如果输入字符串有效，则返回对应的 Python 列表，否则返回 None。
    """
    if input_string is None:
        return None

    try:
        # 将输入字符串中的单引号替换为双引号，以满足 JSON 格式的要求
        input_string = input_string.replace("'", "\"")
        data = json.loads(input_string)
        return data
    except json.JSONDecodeError:
        print("Error: Invalid JSON string")
        return None

category_and_product_list = read_string_to_list(category_and_product_response_1)
print(category_and_product_list)
product_information_for_user_message_1 = generate_output_string(category_and_product_list)
print(product_information_for_user_message_1)

system_message = f"""
您是一家大型电子商店的客服助理。
请以友好和乐于助人的口吻回答问题，并尽量简洁明了。
请确保向用户提出相关的后续问题。
"""

user_message_1 = f"""
请告诉我关于 smartx pro phone 和 the fotosnap camera 的信息。
另外，请告诉我关于你们的tvs的情况。
"""

messages =  [{'role':'system','content': system_message},
             {'role':'user','content': user_message_1},  
             {'role':'assistant',
              'content': f"""相关产品信息:\n\
              {product_information_for_user_message_1}"""}]

final_response = get_completion_from_messages(messages)
print(final_response)






