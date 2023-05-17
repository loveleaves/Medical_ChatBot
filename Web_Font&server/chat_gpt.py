import openai
import random
import requests

from config import *

openai.api_key = key_settings['openai_api_key']

# Q&A bot
# start_sequence = "\nA:"
# restart_sequence = "\n\nQ: "

# open_ended conversation
start_sequence = "\nAI: "
restart_sequence = "\nHuman: "

"""
# if you want to generate prompts automatically, please use the flowing codes.

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
# generate prompt
tokenizer = AutoTokenizer.from_pretrained("merve/chatgpt-prompts-bart-long")
model = AutoModelForSeq2SeqLM.from_pretrained("merve/chatgpt-prompts-bart-long", from_tf=True)
def generate(prompt):
    batch = tokenizer(prompt, return_tensors="pt")
    generated_ids = model.generate(batch["input_ids"], max_new_tokens=150)
    output = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)
    return output[0]
examples = [["photographer"], ["developer"]]
ans = generate(examples[0][0])
"""


def Role_Settings(default_setting=""):
    if default_setting == "":
        # role : capable Q&A bot
        # role_setting = "I am a highly intelligent question answering bot. " \
        #                "If you ask me a question that is rooted in truth, I will give you the answer. " \
        #                "If you ask me a question that is nonsense, trickery, or has no clear answer, " \
        #                "I will respond with \"Unknown\"."
        # role : doctor
        role_setting = "我想让你扮演一名医生，为疾病想出创造性的治疗方法。" \
                       "你应该能够推荐传统药物、草药和其他天然替代品。在提供建议时，你还需要考虑患者的年龄、生活方式和病史。"
    else:
        role_setting = default_setting.strip()
    return role_setting + "\n"


def More_Examples(examples=[]):
    """
    Give more examples to specify.
    """
    if examples == []:
        example1 = ["你好，你是谁？", "我是OpenAI创造的人工智能。有什么需要我帮忙的吗？"]
        examples.append(example1)
    total_example = ""
    for example in examples:
        total_example += restart_sequence + example[0] + start_sequence + example[1]
    return total_example


def GPT_direct(question):
    """
    直接调用 openai 提供的接口
    构造 Prompts 优化回答，更多详见我的仓库
    Github : https://github.com/loveleaves/awesome-chatgpt
    """
    Prompts = restart_sequence + question.strip() + start_sequence
    Prompts = Role_Settings() + More_Examples() + Prompts
    # get response
    response = openai.Completion.create(
        model="text-davinci-003",  # GPT model
        prompt=Prompts,
        temperature=0.6,
        max_tokens=200,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )
    # extract response
    response = dict(response)
    response = response['choices'][0]['text']
    if response == "":
        response = random.choice(gossip_corpus.get('deny'))
    return response


def huggingface(question):
    """
    调用我部署在huggingface上的API
    若报错，则可能我项目设置为Private（应该改为Public）或我openai.api_key过期
    """
    try:
        response = requests.post("https://loveleaves2012-chatgpt.hf.space/run/predict", json={
            "data": [
                question,
            ]
        }).json()
        if isinstance(response, list):
            return response[0]
        else:
            return response
    except:
        data = {'data': None}
        return data


def ChatGPT(question, Direct=False):
    """
    function for Q&A of ChatGPT.
    Learn more about ChatGPT, see my Github repository.
    Github : https://github.com/loveleaves/awesome-chatgpt
    """
    if Direct:
        return GPT_direct(question)
    else:
        return huggingface(question)


if __name__ == "__main__":
    question = "心脏病怎么治疗？"
    ans = ChatGPT(question)
    print(ans)
