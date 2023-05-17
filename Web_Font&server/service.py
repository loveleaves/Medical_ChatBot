# -*- coding:utf-8 -*-
import flask
from flask import request
from gevent import pywsgi

from entity_normalization.app import EMM_model
from knowledge_extraction.bilstm_crf.app import NER_model
from nlu.bert_intent_recognition.app import IR_model
from config import service_settings

app = flask.Flask(__name__)


@app.route("/service/api/medical_en", methods=["GET", "POST"])
def medical_en():
    """
    function: 提供实体规范化服务
    return：
        成功：{"sucess": 1, "data": normalized_entity}
        失败：{"sucess": 0, "data": None}
    """
    data = {"sucess": 0}
    data["data"] = None
    if request.method == "POST":
        try:
            param = flask.request.get_json()
            text = param["text"]
            e_type = param["type"]
            result = EMM_model(text, e_type)
            print(result)

            data["data"] = result
            data["sucess"] = 1
        except:
            pass
        return flask.jsonify(data)

    else:
        try:
            text = request.args.get("text")
            result = EMM_model(text)
            # print(result)
            data["sucess"] = 1
            data["data"] = result
        except:
            pass
        return flask.jsonify(data)


@app.route("/service/api/medical_ner", methods=["GET", "POST"])
def medical_ner():
    """
    function: 提供命名实体识别服务
    return：
        成功：{"sucess": 1, "data": ["string":text,{"entities":[{"type":type,"word":word}],"recog_label":"model"},...]}
        失败：{"sucess": 0, "data": None}
    """
    data = {"sucess": 0}
    data["data"] = None
    if request.method == "POST":
        try:
            text_list = flask.request.get_json()["text_list"]
            # 仅支持单文本输入，多文本取第一个文本
            if isinstance(text_list, list):
                text_list = text_list[0]
            result = NER_model(text_list)
            print(result)
            data["data"] = result
            data["sucess"] = 1
        except:
            pass
        return flask.jsonify(data)

    else:
        try:
            text = request.args.get("text")
            result = NER_model(text)
            # print(result)
            data["data"] = result
            data["sucess"] = 1
        except:
            pass
        return flask.jsonify(data)


@app.route("/service/api/medical_ir", methods=["GET", "POST"])
def medical_ir():
    """
    function: 提供用户问句意图识别服务
    return：
        成功：{"sucess": 1, "data": {"confidence":confidence,"name":IR_type}}
        失败：{"sucess": 0, "data": None}
    """
    data = {"sucess": 0}
    data["data"] = None
    if request.method == "POST":
        try:
            text = flask.request.get_json()["text"]
            # print(param)
            result = IR_model(text)
            print(result)
            data["data"] = result
            data["sucess"] = 1
        except:
            pass
        return flask.jsonify(data)

    else:
        try:
            text = request.args.get("text")
            result = IR_model(text)
            # print(result)
            data["data"] = result
            data["sucess"] = 1
        except:
            pass
        return flask.jsonify(data)


if __name__ == '__main__':
    service_port = service_settings['host_port']
    service_address = service_settings['host_address']
    server = pywsgi.WSGIServer((service_address, service_port), app)
    server.serve_forever()
