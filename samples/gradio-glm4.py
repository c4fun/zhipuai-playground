from zhipuai import ZhipuAI
import gradio as gr

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the value of the API key from the environment variable
api_key = os.getenv("ZHIPUAI_API_KEY")

client = ZhipuAI(api_key=api_key)

def predict(message, history):
    history_zhipuai_format = []
    for human, assistant in history:
        history_zhipuai_format.append({"role": "user", "content": human })
        history_zhipuai_format.append({"role": "assistant", "content":assistant})
    history_zhipuai_format.append({"role": "user", "content": message})
    print(f'history_zhipuai_format: {history_zhipuai_format}')

    # print(history_zhipuai_format)

    response = client.chat.completions.create(
        model='glm-4',
        messages= history_zhipuai_format,
        stream=True
    )

    partial_message = ""
    for chunk in response:
        if len(chunk.choices[0].delta.content) != 0:
            partial_message = partial_message + chunk.choices[0].delta.content
            yield partial_message

           
if __name__ == "__main__":
    gr.ChatInterface(
        fn=predict, 
        chatbot=gr.Chatbot(height="100%"),
        examples=[
"李白的静夜诗写一个",
"""
你是一名擅长创作祝福语的作家，请根据以下要求创作一条给朋友的春节祝福语：
祝福语主题：朋友
祝福语内容：表达对朋友的新年祝福和友情的珍视
生肖：龙年
要求：
祝福语需要反映出对春节的庆祝和对朋友的祝福。
祝福语应该简洁明快，富有节日气氛。
增加emoji。
""",
"""
你是一名擅长创作祝福语的作家，请根据以下要求创作一条给领导的春节祝福语：
祝福语主题：领导
祝福语内容：表达对领导的新年祝福和友情的珍视
生肖：龙年
要求：
祝福语需要反映出对春节的庆祝和对领导的祝福。
祝福语应该简洁明快，富有节日气氛。
增加emoji。
""",
"""
你是一名擅长创作祝福语的作家，请根据以下要求创作一条给家人的春节祝福语：
祝福语内容：表达对舅舅的新年祝福和亲情的特殊
生肖：龙年
要求：
祝福语需要反映出对春节的庆祝和对舅舅的祝福。
祝福语应该简洁明快，富有节日气氛。
增加emoji。
""",
"""
你是一名擅长创作祝福语的作家，请根据以下要求创作一条给发小的春节祝福语：
祝福语内容：表达对发小的新年祝福和对之前咨询问题的感谢
生肖：甲辰龙年
要求：
- 祝福语应该自然一点。
- 增加emoji。
""",
"""
你是一名擅长创作祝福语的作家，请根据以下要求创作一条给前同事的春节祝福语：
祝福语内容：表达对之前工作上的合作的感谢，对同事的新年祝福。
生肖：甲辰龙年
要求：
- 祝福语应该自然一点。
""",
"""
你是一名擅长创作祝福语的作家，请根据以下要求和同事发送的祝福，回复一条给前同事的春节祝福语：
祝福语内容：表达对之前工作上的合作的感谢，对同事的新年祝福。
生肖：甲辰龙年
要求：可以在末尾加上emoji。
同事祝福信息：
XX，感恩YY公司遇见，感谢曾经在ZZ团队做出的努力和贡献。值此龙年新春来临之际，AA祝您和您的家人安康顺遂，福运满满，龙年大吉！[Fireworks][Fireworks][Fireworks][Firecracker][Firecracker][Firecracker]
""",
            ], 
        title="GLM4 bot"
    ).launch()

    # Not working
    # with gr.Blocks() as demo:
    #     with gr.Row():
    #         gr.ChatInterface(fn=predict, height="100%")

    # demo.launch()

    # Not working
    # with gr.Blocks() as demo:
    #     with gr.Row():
    #         gr.Chatbot(fn=predict, id="chat", placeholder="Message", height="100%")

    # demo.launch()