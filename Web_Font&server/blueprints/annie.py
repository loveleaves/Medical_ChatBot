# -*- coding: utf-8 -*-
from flask import Blueprint, request, render_template, session

from chat_annie import annie_replay
from decorators import login_required

bp = Blueprint("annie", __name__, url_prefix="/annie")


# Annie问答主页面
@bp.route("/")
@login_required
def medical_chatbot():
    return render_template("medical_chatbot.html")


# Annie数据处理
@bp.route("/get", methods=["GET", 'POST'])
@login_required
def get_bot_response():
    if request.method == "GET":
        userText = request.args.get('msg')
        user = session.get("user_id")
        return annie_replay(user, userText)
