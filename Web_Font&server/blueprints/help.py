from flask import Blueprint,render_template,request,session, redirect, url_for

from decorators import login_required
from utils.csv_utils import QuestionForm, is_null

bp = Blueprint("help", __name__, url_prefix="/help")

# 帮助首页
@bp.route('/', methods=["POST", "GET"])
@login_required
def help():
    if request.method == "POST":
        form = dict()
        form['title'] = request.form['title']
        form['content'] = request.form['content']
        form['user'] = session.get("user_id")
        Form = QuestionForm(form['user'])
        message = Form.store_question(form['title'], form['content'])
        return render_template("help.html", message=message)

    else:
        return render_template("help.html")

@bp.route("/personal_info", methods=["POST", "GET"])
@login_required
def personal_info():
    if request.method == "POST":
        return render_template("personal_info.html")
    else:
        user = session.get("user_id")
        Form = QuestionForm(user)
        questions = Form.get_user_question()
        return render_template("personal_info.html", questions=questions)

@bp.route("/search")
@login_required
def search():
    """
    function : 话题搜索功能（待实现）
    """
    q = request.args.get("q")
    questions = ""
    # return render_template("index", questions=questions)
    return render_template("todo.html")
