# -*- coding:utf-8 -*-
import flask
import random
import time
import os
import base64
from flask import request
from gevent import pywsgi

from chat_annie import annie_replay
from chat_gpt import ChatGPT
from config import chatbot_service_settings, chatgpt_corpus
from asr_tts.asr import YouDaoASRAPI
from asr_tts.tts import YouDaoTTSAPI

app = flask.Flask(__name__)

youdao_asr = YouDaoASRAPI()
youdao_tts = YouDaoTTSAPI()


@app.route("/service/api/medical_asr", methods=["GET", "POST"])
def medical_asr():
    """
    function: 提供ASR自动语音识别服务
    return：
        成功：{"sucess": 1, "data": answer}
        失败：{"sucess": 0, "data": None}
    """
    if request.method == "POST":
        pass


@app.route("/service/api/medical_tts", methods=["GET", "POST"])
def medical_tts():
    """
    function: 提供TTS文本转语音服务
    return：
        成功：{"sucess": 1, "data": answer}
        失败：{"sucess": 0, "data": None}
    """
    if request.method == "POST":
        pass


@app.route("/service/api/medical_annie", methods=["GET", "POST"])
def medical_annie():
    """
    function: 为小程序等用户端提供Annie的问答服务
    Note : 勿放入service.py中引起错误
    return：
        成功：{"sucess": 1, "data": answer}
        失败：{"sucess": 0, "data": None}
    """
    data = {"sucess": 0}
    data["data"] = None
    if request.method == "POST":
        try:
            # 以下为处理文本POST，弃用
            # text = flask.request.get_json()["text"]
            # user = flask.request.get_json()["user"]
            user = request.form.get("username")
            audio_file = request.files['recordFile']
            # 直接编码为base64后面有到翻译时出错，暂未知其原因，待解决 TODO
            # base64_str = base64.b64encode(audio_file.stream.read()).decode()
            # asr_ans = youdao_asr.asr(sample_rate=16000, nchannels=1,base64_str=base64_str)

            # 以下为先存储为文件再处理
            millis = int(round(time.time() * 1000))
            audio_file_path = "logs/" + str(millis) + ".wav"
            if os.path.exists(audio_file_path):
                os.system("rm -rf " + audio_file_path)
            audio_file.save(audio_file_path)
            asr_ans = youdao_asr.asr(audio_from_file=True, audio_file_path=audio_file_path)
            print("语音识别结果：", asr_ans)

            result = annie_replay(user, asr_ans)
            print("Annie回答结果：", result)

            tts_file_path = "logs/" + str(millis) + ".mp3"
            if os.path.exists(tts_file_path):
                os.system("rm -rf " + tts_file_path)
            youdao_tts.tts(q=result, tts_file_path=tts_file_path)
            with open(tts_file_path, 'rb') as f:
                audio_data_str = base64.b64encode(f.read()).decode()

            data["data"] = audio_data_str
            data["sucess"] = 1
        except:
            pass
        return flask.jsonify(data)

    else:
        result = "暂不提供该类型请求！"
        data["sucess"] = 1
        data["data"] = result
        return flask.jsonify(data)


@app.route("/service/api/medical_gpt", methods=["GET", "POST"])
def medical_gpt():
    """
    function: 为小程序等用户端提供ChatGPT的问答服务
    Note : 勿放入service.py中引起错误
    return：
        成功：{"sucess": 1, "data": answer}
        失败：{"sucess": 0, "data": None}
    """
    data = {"sucess": 0}
    data["data"] = None
    if request.method == "POST":
        try:
            text = flask.request.get_json()["text"]
            user = flask.request.get_json()["user"]
            ans = ChatGPT(text)
            if ans['data']:
                if isinstance(ans['data'], str):
                    result = ans['data']
                elif isinstance(ans['data'], list):
                    result = ''.join(ans['data'])
                else:
                    result = "ChatGPT返回类型错误！"

            else:
                # return random.choice(chatgpt_corpus.get('deny'))
                return "无法连接到ChatGPT服务器，请重试"
            print(result)
            data["data"] = result
            data["sucess"] = 1
        except:
            pass
        return flask.jsonify(data)

    else:
        result = "暂不提供该类型请求！"
        data["sucess"] = 1
        data["data"] = result
        return flask.jsonify(data)


if __name__ == '__main__':
    service_port = chatbot_service_settings['host_port']
    service_address = chatbot_service_settings['host_address']
    server = pywsgi.WSGIServer((service_address, service_port), app)
    server.serve_forever()
