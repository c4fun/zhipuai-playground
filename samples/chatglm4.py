import time
from zhipuai import ZhipuAI

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the value of the API key from the environment variable
api_key = os.getenv("ZHIPUAI_API_KEY")

client = ZhipuAI(api_key=api_key)

def invoke():
    response = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=[
            {"role": "user", "content": "你好"},
            {"role": "assistant", "content": "我是人工智能助手"},
            {"role": "user", "content": "你叫什么名字"},
            {"role": "assistant", "content": "我叫chatGLM"},
            {"role": "user", "content": "你都可以做些什么事"}
        ],
    )
    print(response.choices[0].message)


def async_invoke():
    response = client.chat.asyncCompletions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=[
            {
                "role": "user",
                "content": "请你作为童话故事大王，写一篇短篇童话故事，故事的主题是要永远保持一颗善良的心，要能够激发儿童的学习兴趣和想象力，同时也能够帮助儿童更好地理解和接受故事中所蕴含的道理和价值观。"
            }
        ],
    )
    print(response)
    time.sleep(40)
    print(response)
            
def sse():
    response = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=[
            {"role": "system", "content": "你是一个人工智能助手，你叫叫chatGLM"},
            {"role": "user", "content": "你好！你叫什么名字"},
        ],
        stream=True,
    )
    for chunk in response:
        print(chunk.choices[0].delta)    


if __name__ == '__main__':
    invoke()
    # async_invoke()
    # sse()