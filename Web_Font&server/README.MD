## Medical_ChatBot_Font&BK_Management

## 项目介绍

> 该项目是问答系统的前端和后台（前后端未分离），由Flask+Bootstrap+Neo4j等实现。

## 项目环境



## 目录结构

```markdown
Web_Font&bkManagement
│  app.py  # Web前端主程序
│  chatbot_service.py  # 聊天服务主程序
│  chat_annie.py
│  chat_gpt.py
│  config.py  # 主配置文件
│  decorators.py
│  modules.py
│  package_management.py
│  service.py  # 问答系统功能服务主程序
│  
├─asr_tts
│      asr.py
│      config.py
│      tts.py
│      utils.py
│      __init__.py
│      
├─blueprints
│      admin.py
│      annie.py
│      api.py
│      auth.py
│      chat_gpt.py
│      help.py
│      index.py
│      __init__.py
│      
├─build_kg
│  │  build_kg_utils.py
│  │  
│  ├─graph_data
│  └─prepare_data
│          data_example.json
│          data_spider.py
│          fusion_utils.py
│          prepare_alias.py
│          preprocess_data.py
│          spider_utils.py
│          
├─db
├─docs
│      Flask基础知识.md
│      README.MD
│      
├─entity_normalization
│  │  app.py
│  │  bm25_retrival.py
│  │  config.py
│  │  data_helper.py
│  │  esim.py
│  │  predict.py
│  │  train.py
│  │  __init__.py
│  │  
│  ├─checkpoint
│  ├─CHIP-CDN
│  ├─data
│  ├─total
│  └─yidu-n7k
├─knowledge_extraction
│  │  __init__.py
│  │  
│  ├─bert_for_ner
│  │  │  app.py
│  │  │  build_model.py
│  │  │  config.py
│  │  │  data_utils.py
│  │  │  eval.py
│  │  │  metrics.py
│  │  │  train.py
│  │  │  
│  │  ├─checkpoint
│  │  └─data
│  └─bilstm_crf
│      │  app.py
│      │  bilstm_crf_model.py
│      │  config.py
│      │  crf_layer.py
│      │  data_helpers.py
│      │  data_preprocess.py
│      │  metrics.py
│      │  test.py
│      │  train.py
│      │  __init__.py
│      │  
│      ├─checkpoint
│      ├─cMedQA2
│      ├─cMedQANER
│      ├─CMID
│      ├─data
│      ├─DIY_data
│      └─yidu-s4k
├─logs
├─nlu
│  │  __init__.py
│  │  
│  ├─bert_intent_recognition
│  │  │  app.py
│  │  │  bert_model.py
│  │  │  config.py
│  │  │  data_helper.py
│  │  │  test.py
│  │  │  train.py
│  │  │  __init__.py
│  │  │  
│  │  ├─bert_weight_files
│  │  │  └─bert_wwm
│  │  ├─checkpoint
│  │  ├─data
│  │  └─raw_data
│  └─sklearn_Classification
│      │  clf_model.py
│      │  train.py
│      │  
│      ├─data
│      └─model_file
├─static
│  ├─bootstrap
│  │      bootstrap.4.6.min.css
│  │      
│  ├─css
│  │      chat.css
│  │      init.css
│  │      style.css
│  │      
│  └─images
│          404.gif
│          avatar.jpg
│          bg.jpg
│          doctor.png
│          login.jpg
│          loginbg.png
│          openai.png
│          user.png
│          
├─templates
│      404.html
│      admin_base.html
│      admin_index.html
│      admin_info.html
│      admin_question.html
│      admin_user.html
│      admin_visual.html
│      base.html
│      chat_gpt.html
│      help.html
│      index.html
│      login.html
│      medical_chatbot.html
│      personal_info.html
│      register.html
│      todo.html
│      
└─utils
        cpubmed_api_utils.py
        csv_utils.py
        json_utils.py
        log_handler.py
        SimHei.ttf
        visual_utils.py
        __init__.py
```

## 开源协议

Medical_ChatBot采用MIT license，详情见[MIT LICENSE](./LICENSE)。