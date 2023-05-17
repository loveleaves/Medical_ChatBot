# -*- coding:utf-8 -*-
from flask import Flask, session, g, render_template
from gevent import pywsgi

from blueprints.auth import bp as auth_bp
from blueprints.annie import bp as annie_bp
from blueprints.chat_gpt import bp as chatgpt_bp
from blueprints.index import bp as index_bp
from blueprints.help import bp as help_bp
from blueprints.api import bp as api_bp
from blueprints.admin import bp as admin_bp
from config import key_settings

# 开启一个flask应用
app = Flask(__name__)
app.secret_key = key_settings['app_secret_key']

# 蓝图注册
app.register_blueprint(auth_bp)
app.register_blueprint(annie_bp)
app.register_blueprint(chatgpt_bp)
app.register_blueprint(index_bp)
app.register_blueprint(help_bp)
app.register_blueprint(api_bp)
app.register_blueprint(admin_bp)

"""
hook : before_request/ before_first_request / after_request
"""


@app.before_request
def my_before_request():
    user = session.get("user_id")
    # 用于识别管理员
    if user == key_settings['admin_user']:
        setattr(g, "admin", user)
    else:
        setattr(g, "admin", None)
    # 用于识别用户
    if user:
        setattr(g, "user", user)
    else:
        setattr(g, "user", None)


@app.context_processor
def my_context_processor():
    return {"user": g.user}


# 404页面
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# 500页面
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('404.html'), 500


if __name__ == '__main__':
    # 本地运行
    # app.run()
    # 本网段内可访问
    # app.run("0.0.0.0", 5000)

    server = pywsgi.WSGIServer(("0.0.0.0", 5000), app)
    server.serve_forever()
