'''
检查结果
运用审查(Moderation) API 来评估系统生成的输出
'''
import openai
from utils.tools import get_completion_from_messages

final_response_to_customer = f"""
SmartX ProPhone 有一个 6.1 英寸的显示屏，128GB 存储、\
1200 万像素的双摄像头，以及 5G。FotoSnap 单反相机\
有一个 2420 万像素的传感器，1080p 视频，3 英寸 LCD 和\
可更换的镜头。我们有各种电视，包括 CineView 4K 电视，\
55 英寸显示屏，4K 分辨率、HDR，以及智能电视功能。\
我们也有 SoundMax 家庭影院系统，具有 5.1 声道，\
1000W 输出，无线重低音扬声器和蓝牙。关于这些产品或\
我们提供的任何其他产品您是否有任何具体问题？
"""
# Moderation 是 OpenAI 的内容审核函数，旨在评估并检测文本内容中的潜在风险。
response = openai.Moderation.create(
    input=final_response_to_customer
)
moderation_output = response["results"][0]
print(moderation_output)
