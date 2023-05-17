from functools import wraps
from flask import g, redirect, url_for

from utils.csv_utils import config

def login_required(func):
    # 保留func的信息
    # flask下下面"@wraps"必须写
    @wraps(func)
    def inner(*args, **kwargs):
        if g.user:
            return func(*args, **kwargs)
        else:
            return redirect(url_for("auth.user_login"))
    return inner

def logout_required(func):
    # 保留func的信息
    # flask下下面"@wraps"必须写
    @wraps(func)
    def inner(*args, **kwargs):
        if not g.user:
            return func(*args, **kwargs)
        else:
            return redirect("/")

    return inner

def admin_required(func):
    # 保留func的信息
    # flask下下面"@wraps"必须写
    @wraps(func)
    def inner(*args, **kwargs):
        if g.admin:
            return func(*args, **kwargs)
        else:
            if g.user:
                return redirect("/")
            else:
                return redirect(url_for("auth.user_login"))

    return inner