from flask import Blueprint, render_template, redirect, url_for, request, template_rendered

# from decorators import login_required

bp = Blueprint("index", __name__, url_prefix="/")


# 首页
@bp.route('/')
def index():
    return render_template('index.html')
