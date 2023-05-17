# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, session
import random

from chat_gpt import ChatGPT
from config import chatgpt_corpus
from decorators import login_required
from utils.csv_utils import change_user_content, get_user_content

bp = Blueprint("chat_gpt", __name__, url_prefix="/chat_gpt")


# ChatGPT问答主页面
@bp.route("/")
@login_required
def chat_gpt():
    return render_template("chat_gpt.html")


# Annie数据处理
@bp.route("/get")
@login_required
def get_chatgpt_response():
    user = session.get("user_id")
    userText = request.args.get('msg')
    chat_gpt_use_times = get_user_content(user, chat_gpt_use_times=True)[0]

    if chat_gpt_use_times > 0 or chat_gpt_use_times == -3:
        ans = ChatGPT(userText)
        print(ans)
        if ans['data']:
            change_user_content(user, chat_gpt_use_times="-1")
            if isinstance(ans['data'], str):
                return ans['data']
            elif isinstance(ans['data'], list):
                return ''.join(ans['data'])
            else:
                return "ChatGPT返回类型错误！"

        else:
            # return random.choice(chatgpt_corpus.get('deny'))
            return "无法连接到ChatGPT服务器，请重试"
    else:
        return "5次机会已用完"
