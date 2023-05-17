# -*- coding:utf-8 -*-
import random

from modules import gossip_robot, medical_robot, classifier
from utils.json_utils import dump_user_dialogue_context, load_user_dialogue_context
from config import default_answer

# Annie问答主处理程序
def annie_replay(user: str, msg: str):
    assert user != "", "用户名不能为空"

    user_intent = classifier(msg)
    if user_intent in ["greet", "goodbye", "deny", "isbot"]:
        reply = gossip_robot(user_intent)
    elif user_intent == "accept":
        reply = load_user_dialogue_context(user)
        reply = reply.get("choice_answer", "")
    else:
        reply = medical_robot(msg, user)
        if reply["slot_values"]:
            dump_user_dialogue_context(user, reply)
        reply = reply.get("replay_answer", "")

    if '\n' in reply:
        reply = reply.strip().replace('\n', '<br/>')
    # print(reply)
    if reply.strip():
        return reply
    else:
        return random.choice(default_answer)
