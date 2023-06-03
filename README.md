# Medical_ChatBot
## 项目名称

基于知识图谱的医疗健康问答系统  [Github](https://github.com/loveleaves/Medical_ChatBot) 

## 项目介绍

> 功能：本系统能实现常见疾病相关的文本和语音问答。
>
> 构成：本项目V3.x共包含四个部分，分别为问答系统的Web前端、小程序前端、服务后端和小程序后台管理前端，改由tensorflow2.5开发而成，支持GPU训练及推理。

## 项目计划内容

- [x] “命名实体识别”改为BERT-CRF，支持GPU
- [x] “实体规范化”改为支持GPU
- [ ] “用户问句意图识别”改为BERT-TextCNN，支持GPU
- [ ] “实体规范化” BM25召回算法 改为 faiss等测试
- [ ] 前端Web界面改用Vue3.x开发
- [ ] 后端模型运行框架改用FastAPI等测试

### 设计思路

本系统基于KBQA（基于知识图谱的问答）和TODS（任务型对话系统）实现的基于深度学习的、检索式的、任务型导向的问答系统。

### 项目效果



### 目录结构



### 部署教程



## 开源协议

Medical_ChatBot采用MIT license，详情见[MIT LICENSE](./LICENSE)。