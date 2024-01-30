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
        examples=["李白的静夜诗写一个"], 
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