# -*- coding:utf-8 -*-

key_settings = {
    "openai_api_key": "sk-#",  #  your openai_api_key
    "app_secret_key": '#', # your app_secret_key
    "admin_user": "admin",
}

neo4j_settings = { # your neo4j settings
    "host": "127.0.0.1",
    "http_port": 7474,
    "user": "neo4j",
    "password": "123456",
}

service_settings = { # chatbot module settings
    "host_port": 60061,
    #"host_address": "127.0.0.1",
    "host_address": "0.0.0.0",
    "host_url": "http://127.0.0.1:60061/service/api/"
}

chatbot_service_settings = { # chatbot service settings
    "host_port": 60062,
    "host_address": "0.0.0.0",
    "host_url": "http://127.0.0.1:60062/service/api/"
}

semantic_slot = {
    "定义": {
        "slot_list": ["Disease"],
        "slot_values": None,
        "cql_template": "MATCH(p:疾病) WHERE p.name='{Disease}' RETURN p.desc",
        "reply_template": "'{Disease}' 是这样的：\n",
        "ask_template": "您问的是 '{Disease}' 的定义吗？",
        "intent_strategy": "",
        "deny_response": "很抱歉没有理解你的意思呢~"
    },
    "病因": {
        "slot_list": ["Disease"],
        "slot_values": None,
        "cql_template": "MATCH(p:疾病) WHERE p.name='{Disease}' RETURN p.cause",
        "reply_template": "'{Disease}' 疾病的原因是：\n",
        "ask_template": "您问的是疾病 '{Disease}' 的原因吗？",
        "intent_strategy": "",
        "deny_response": "您说的我有点不明白，您可以换个问法问我哦~"
    },
    "预防": {
        "slot_list": ["Disease"],
        "slot_values": None,
        "cql_template": "MATCH(p:疾病) WHERE p.name='{Disease}' RETURN p.prevent",
        "reply_template": "关于 '{Disease}' 疾病您可以这样预防：\n",
        "ask_template": "请问您问的是疾病 '{Disease}' 的预防措施吗？",
        "intent_strategy": "",
        "deny_response": "额~似乎有点不理解你说的是啥呢~"
    },
    "临床表现(病症表现)": {
        "slot_list": ["Disease"],
        "slot_values": None,
        "cql_template": "MATCH(p:疾病)-[r:has_symptom]->(q:症状) WHERE p.name='{Disease}' RETURN q.name",
        "reply_template": "'{Disease}' 疾病的病症表现一般是这样的：\n",
        "ask_template": "您问的是疾病 '{Disease}' 的症状表现吗？",
        "intent_strategy": "",
        "deny_response": "人类的语言太难了！！"
    },
    "相关病症": {
        "slot_list": ["Disease"],
        "slot_values": None,
        "cql_template": "MATCH(p:疾病)-[r:acompany_with]->(q:疾病) WHERE p.name='{Disease}' RETURN q.name",
        "reply_template": "'{Disease}' 疾病的具有以下并发疾病：\n",
        "ask_template": "您问的是疾病 '{Disease}' 的并发疾病吗？",
        "intent_strategy": "",
        "deny_response": "人类的语言太难了！！~"
    },
    # “治疗方法”数据与下面部分数据冲突，待解决 TODO
    "治疗方法": {
        "slot_list": ["Disease"],
        "slot_values": None,
        "cql_template": ["MATCH(p:疾病) WHERE p.name='{Disease}' RETURN p.cure_way",
                         "MATCH(p:疾病)-[r:recommand_drug]->(q) WHERE p.name='{Disease}' RETURN q.name",
                         "MATCH(p:疾病)-[r:recommand_recipes]->(q) WHERE p.name='{Disease}' RETURN q.name"],
        "reply_template": "'{Disease}' 疾病的治疗方式、可用的药物、推荐菜肴有：\n",
        "ask_template": "您问的是疾病 '{Disease}' 的治疗方法吗？",
        "intent_strategy": "",
        "deny_response": "没有理解您说的意思哦~"
    },
    "所属科室": {
        "slot_list": ["Disease"],
        "slot_values": None,
        "cql_template": "MATCH(p:疾病)-[r:cure_department]->(q:科室) WHERE p.name='{Disease}' RETURN q.name",
        "reply_template": "得了 '{Disease}' 可以挂这个科室哦：\n",
        "ask_template": "您想问的是疾病 '{Disease}' 要挂什么科室吗？",
        "intent_strategy": "",
        "deny_response": "您说的我有点不明白，您可以换个问法问我哦~"
    },
    "传染性": {
        "slot_list": ["Disease"],
        "slot_values": None,
        "cql_template": "MATCH(p:疾病) WHERE p.name='{Disease}' RETURN p.easy_get",
        "reply_template": "'{Disease}' 较为容易感染这些人群：\n",
        "ask_template": "您想问的是疾病 '{Disease}' 会感染哪些人吗？",
        "intent_strategy": "",
        "deny_response": "没有理解您说的意思哦~"
    },
    "治愈率": {
        "slot_list": ["Disease"],
        "slot_values": None,
        "cql_template": "MATCH(p:疾病) WHERE p.name='{Disease}' RETURN p.cured_prob",
        "reply_template": "得了'{Disease}' 的治愈率为：",
        "ask_template": "您想问 '{Disease}' 的治愈率吗？",
        "intent_strategy": "",
        "deny_response": "您说的我有点不明白，您可以换个问法问我哦~"
    },
    "治疗时间": {
        "slot_list": ["Disease"],
        "slot_values": None,
        "cql_template": "MATCH(p:疾病) WHERE p.name='{Disease}' RETURN p.cure_lasttime",
        "reply_template": "疾病 '{Disease}' 的治疗周期为：",
        "ask_template": "您想问 '{Disease}' 的治疗周期吗？",
        "intent_strategy": "",
        "deny_response": "很抱歉没有理解你的意思呢~"
    },
    "化验/体检方案": {
        "slot_list": ["Disease"],
        "slot_values": None,
        "cql_template": "MATCH(p:疾病)-[r:need_check]->(q:检查) WHERE p.name='{Disease}' RETURN q.name",
        "reply_template": "得了 '{Disease}' 需要做以下检查：\n",
        "ask_template": "您是想问 '{Disease}' 要做什么检查吗？",
        "intent_strategy": "",
        "deny_response": "您说的我有点不明白，您可以换个问法问我哦~"
    },
    "禁忌": {
        "slot_list": ["Disease"],
        "slot_values": None,
        "cql_template": "MATCH(p:疾病)-[r:not_eat]->(q:食物) WHERE p.name='{Disease}' RETURN q.name",
        "reply_template": "得了 '{Disease}' 切记不要吃这些食物哦：\n",
        "ask_template": "您是想问 '{Disease}' 不可以吃的食物是什么吗？",
        "intent_strategy": "",
        "deny_response": "额~似乎有点不理解你说的是啥呢~~"
    },
    "患病概率": {
        "slot_list": ["Disease"],
        "slot_values": None,
        "cql_template": "MATCH(p:疾病) WHERE p.name='{Disease}' RETURN p.get_prob",
        "reply_template": " '{Disease}' 疾病的患病概率为：\n",
        "ask_template": "请问您问的是疾病 '{Disease}' 的患病率吗？",
        "intent_strategy": "",
        "deny_response": "您说的我有点不明白，您可以换个问法问我哦~"
    },
    "推荐食物": {
        "slot_list": ["Disease"],
        "slot_values": None,
        "cql_template": "MATCH(p:疾病)-[r:do_eat]->(q:食物) WHERE p.name='{Disease}' RETURN q.name",
        "reply_template": "得了 '{Disease}' 推荐吃这些食物哦：\n",
        "ask_template": "您是想问 '{Disease}' 推荐吃的食物是什么吗？",
        "intent_strategy": "",
        "deny_response": "额~似乎有点不理解你说的是啥呢~~"
    },
    "推荐菜谱": {
        "slot_list": ["Disease"],
        "slot_values": None,
        "cql_template": "MATCH(p:疾病)-[r:recommand_recipes]->(q:菜谱) WHERE p.name='{Disease}' RETURN q.name",
        "reply_template": "得了 '{Disease}' 推荐吃这些菜哦：\n",
        "ask_template": "您是想问 '{Disease}' 推荐吃什么菜吗？",
        "intent_strategy": "",
        "deny_response": "很抱歉没有理解你的意思呢~"
    },
    "通用药品": {
        "slot_list": ["Disease"],
        "slot_values": None,
        "cql_template": "MATCH(p:疾病)-[r:has_common_drug]->(q:药品) WHERE p.name='{Disease}' RETURN q.name",
        "reply_template": "得了 '{Disease}' 可以吃这些药哦：\n",
        "ask_template": "您是想问 '{Disease}' 可以吃什么药吗？",
        "intent_strategy": "",
        "deny_response": "非常抱歉，我还不知道如何回答您，我正在努力学习中~"
    },
    "推荐药品": {
        "slot_list": ["Disease"],
        "slot_values": None,
        "cql_template": "MATCH(p:疾病)-[r:recommand_drug]->(q:药品) WHERE p.name='{Disease}' RETURN q.name",
        "reply_template": "得了 '{Disease}' 推荐吃这些药哦：\n",
        "ask_template": "您是想问 '{Disease}' 推荐吃什么药吗？",
        "intent_strategy": "",
        "deny_response": "很抱歉没有理解你的意思呢~"
    },
    "unrecognized": {
        "slot_values": None,
        "replay_answer": "非常抱歉，我还不知道如何回答您，我正在努力学习中~",
    }
}

intent_threshold_config = {
    # 意图识别的结果作为主要决策信息
    "accept": 0.8,
    "deny": 0.4
}

default_answer = [
    "很抱歉我还不知道回答你这个问题。\n你可以问我一些有关疾病的定义、原因、治疗方法、注意事项、挂什么科室预防、禁忌等相关问题哦~",
    "唔~我装满知识的大脑此刻很贫瘠",
    "非常抱歉无法回答您，您可以试着问我其他问题哟～"
]

gossip_corpus = {
    "greet": [
        "hi",
        "你好呀",
        "我是你的私人助理Annie，有什么可以帮助你吗",
        "hi，你好，你可以叫我Annie",
        "你好，你可以问我一些关于疾病诊断的问题哦"
    ],
    "goodbye": [
        "再见，很高兴为您服务",
        "bye",
        "再见，感谢使用我的服务",
        "再见啦，祝你健康"
    ],
    "deny": [
        "很抱歉没帮到您",
        "I am sorry",
        "那您可以试着问我其他问题哟"
    ],
    "isbot": [
        "我是Annie，你的私人医生",
        "你可以叫我Annie哦~",
        "我是你的私人医生Annie"
    ],
}

chatgpt_corpus = {
    "deny": [
        "抱歉，这边网络好像断开了哟～",
        "很抱歉没帮到您",
        "I am sorry"
    ],
}
