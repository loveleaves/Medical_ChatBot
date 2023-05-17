# -*- coding:utf-8 -*-
import json
import requests
import random
from py2neo import Graph

from nlu.sklearn_Classification.clf_model import CLFModel
from utils.json_utils import load_user_dialogue_context
from utils.csv_utils import ChatBotQuestion
from config import *

"""
neo4j Graph db Connection
"""
graph = Graph(host=neo4j_settings['host'],
              http_port=neo4j_settings['http_port'],
              user=neo4j_settings['user'],
              password=neo4j_settings['password'])


def intent_classifier(text):
    """
    function : Intent Recognition
    return : {"name":str,"confidence":float}
    """
    # 连接Flask API接口
    url = service_settings['host_url'] + 'medical_ir'
    data = {"text": text}
    headers = {'Content-Type': 'application/json;charset=utf8'}

    response = requests.post(url,
                             data=json.dumps(data),
                             headers=headers)
    if response.status_code == 200:
        response = json.loads(response.text)
        return response['data']
    else:
        return -1


def slot_recognizer(text):
    """
    function : Medical Named Entity Recognition
    return :
        [{'string': '心', 'entities': [{'word': '心', 'type': 'body'}], 'recog_label': 'model'}, ...]
    """
    url = service_settings['host_url'] + 'medical_ner'
    data = {"text_list": [text]}
    headers = {'Content-Type': 'application/json;charset=utf8'}

    response = requests.post(url,
                             data=json.dumps(data),
                             headers=headers)
    if response.status_code == 200:
        response = json.loads(response.text)
        if not response['sucess']:
            return -1
        response_data = response['data']
        return response_data

    else:
        return -1


def entity_link(mention, etype):
    """
    function :
        对于识别到的实体mention,如果其不是知识库中的标准称谓
        则对其进行实体链指，将其指向一个唯一实体

    params :
        mention : 实体指代
        etype : mention所属类型
    """
    # 连接Flask API接口
    url = service_settings['host_url'] + 'medical_en'
    data = {"text": mention, "type": etype}
    headers = {'Content-Type': 'application/json;charset=utf8'}

    response = requests.post(url,
                             data=json.dumps(data),
                             headers=headers)
    if response.status_code == 200:
        response_data = json.loads(response.text)
        if not response_data['sucess']:
            return -1
        return response_data['data']
    else:
        return None


def classifier(text):
    """
    function : 判断是否是闲聊意图，以及是什么类型闲聊
    """
    clf_model = CLFModel('./nlu/sklearn_Classification/model_file/')
    return clf_model.predict(text)


def neo4j_searcher(cql_list):
    """
    function : CQL construction
    """
    responses = ""
    if isinstance(cql_list, list):
        for cql in cql_list:
            data = graph.run(cql).data()
            if data:
                tmp = []
                for d in data:
                    d = list(d.values())
                    if isinstance(d[0], list):
                        tmp.extend(d[0])
                    else:
                        tmp.extend(d)

                data = "、".join([str(i) for i in tmp])
                responses += data + "\n"
    else:
        data = graph.run(cql_list).data()
        if data:
            tmp = []
            for d in data:
                d = list(d.values())
                if isinstance(d[0], list):
                    tmp.extend(d[0])
                else:
                    tmp.extend(d)

            data = "、".join([str(i) for i in tmp])
            responses += data

    ans = responses.split('\n')
    responses = []
    for item in ans:
        if item == "None":
            responses.append("我暂时还不知道哦～")
        else:
            responses.append(item)
    return "\n".join(responses)


def semantic_parser(text, user):
    """
    function : 对文本进行解析
    return : semantic slot
    """
    intent_data = intent_classifier(text)
    slot_data = slot_recognizer(text)
    # 触及系统intent和slot的知识盲区
    if intent_data == -1 or slot_data == -1 or intent_data.get("name") == "其他":
        return semantic_slot.get("unrecognized")

    # 意图继承
    slot_info = semantic_slot.get(intent_data.get("name"))
    # slot filling
    slots = slot_info.get("slot_list")
    slot_values = {}
    for slot in slots:
        slot_values[slot] = None
        for ent_info in slot_data:
            for e in ent_info["entities"]:
                if slot.lower() == e['type']:
                    entity_link_ans = entity_link(e['word'], e['type'])
                    if entity_link_ans:
                        slot_values[slot] = entity_link_ans
                        slot_info["original_entity"] = e['word']
                    else:
                        slot_values[slot] = e['word']

    last_slot_values = load_user_dialogue_context(user)["slot_values"]
    for k in slot_values.keys():
        if slot_values[k] is None:
            slot_values[k] = last_slot_values.get(k, None)

    slot_info["slot_values"] = slot_values

    # Dialogue Management
    conf = intent_data.get("confidence")
    if conf >= intent_threshold_config["accept"]:
        slot_info["intent_strategy"] = "accept"
    elif conf >= intent_threshold_config["deny"]:
        slot_info["intent_strategy"] = "clarify"
    else:
        slot_info["intent_strategy"] = "deny"

    return slot_info


def get_answer(slot_info):
    """
    function : 根据slot_info构造回复
    """
    cql_template = slot_info.get("cql_template")
    reply_template = slot_info.get("reply_template")
    ask_template = slot_info.get("ask_template")
    slot_values = slot_info.get("slot_values")
    strategy = slot_info.get("intent_strategy")

    if not slot_values:
        return slot_info

    # alias description
    alias_des = ""
    original_entity = slot_info.get("original_entity")
    el_entity = slot_values['Disease']
    if original_entity != el_entity:
        alias_des = f'"{original_entity}"又叫“{el_entity}”。'

    if strategy == "accept":
        cql = []
        if isinstance(cql_template, list):
            for cqlt in cql_template:
                cql.append(cqlt.format(**slot_values))
        else:
            cql = cql_template.format(**slot_values)
        answer = neo4j_searcher(cql)
        if not answer:
            slot_info["replay_answer"] = random.choice(default_answer)
        else:
            pattern = reply_template.format(**slot_values)
            slot_info["replay_answer"] = alias_des + pattern + answer

    elif strategy == "clarify":
        # Information Confirmation
        pattern = ask_template.format(**slot_values)
        slot_info["replay_answer"] = pattern

        cql = []
        if isinstance(cql_template, list):
            for cqlt in cql_template:
                cql.append(cqlt.format(**slot_values))
        else:
            cql = cql_template.format(**slot_values)
        answer = neo4j_searcher(cql)
        if not answer:
            slot_info["replay_answer"] = random.choice(default_answer)
        else:
            pattern = reply_template.format(**slot_values)
            slot_info["choice_answer"] = alias_des + pattern + answer

    elif strategy == "deny":
        slot_info["replay_answer"] = slot_info.get("deny_response")

    return slot_info


def gossip_robot(intent):
    """
    function : gossip mode
    """
    return random.choice(gossip_corpus.get(intent))


def store_question(semantic_slot, user):
    """
    function : store the questions for visualization
    entity label of cMedQANER dataset：{'physiology', 'test', 'disease', 'time', 'drug',
        'symptom', 'body', 'department', 'crowd', 'feature', 'treatment'}
    """
    chatbot_form = ChatBotQuestion()
    if 'slot_values' in semantic_slot.keys() and semantic_slot['slot_values']:
        for entity_type in semantic_slot['slot_list']:
            info = dict()
            info['username'] = user
            info['entity_type'] = entity_type
            info['entity_name'] = semantic_slot['slot_values'][entity_type]

            chatbot_form.store_question_entity(**info)


def medical_robot(question, user):
    """
    function : medical QA mode
    """
    semantic_slot = semantic_parser(question, user)
    store_question(semantic_slot, user)
    answer = get_answer(semantic_slot)
    return answer
