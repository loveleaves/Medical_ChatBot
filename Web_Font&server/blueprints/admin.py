from flask import Blueprint,render_template,redirect,url_for,request, template_rendered, g
from werkzeug.security import check_password_hash

from decorators import admin_required
from utils.csv_utils import get_all_user_content, is_null, change_user_content, QuestionForm, get_user_content

bp = Blueprint("admin", __name__, url_prefix="/admin")

# 管理员首页
@bp.route('/')
@admin_required
def admin_index():
    return render_template('admin_index.html')

# 用户信息管理页面
@bp.route('/user', methods=["POST", "GET"])
@admin_required
def admin_user():
    if request.method == "GET":
        all_user_info = get_all_user_content()
        return render_template("admin_user.html", users=all_user_info)
    else:
        username = request.form['username']
        password = request.form['password']
        PIT = request.form['PIT']
        CGUT = request.form['CGUT']
        # print(username,password,PIT,CGUT)
        if is_null(username,password,PIT, CGUT):
            login_massage = "温馨提示：信息都不能为空！"
            return render_template('admin_user.html', message=login_massage)
        elif not PIT.strip('-').isdigit() or not CGUT.strip('-').isdigit():
            login_massage = "温馨提示：密码允许输入次数和ChatGPT允许使用次数只能输入数字！"
            return render_template('admin_user.html', message=login_massage)
        else:
            login_massage = "温馨提示：修改成功！"
            change_user_content(username, password=password,
                                password_input_times=PIT,chat_gpt_use_times=CGUT)
            return render_template('admin_user.html', message=login_massage)

# 用户信息管理页面
@bp.route('/question', methods=["POST", "GET"])
@admin_required
def admin_question():
    if request.method == "GET":
        Form = QuestionForm("")
        questions = Form.get_all_question()
        return render_template("admin_question.html", questions=questions)
    else:
        username = request.form['username']
        title = request.form['title']
        question = request.form['content']
        answer = request.form['answer']

        Form = QuestionForm(username)
        questions = Form.get_all_question()

        if is_null(title,question,answer):
            login_massage = "温馨提示：内容都不能为空！"
            return render_template('admin_question.html', questions=questions, message=login_massage)

        elif len(title) > 30 or len(question) > 300 or len(answer) > 1000:
            login_massage = "温馨提示：内容过长。"
            return render_template('admin_question.html', questions=questions, message=login_massage)

        else:
            flag = Form.update_answer(title, answer, question=question)
            questions = Form.get_all_question()
            if flag:
                login_massage = "温馨提示：修改成功！"
            else:
                login_massage = "温馨提示：修改失败！"
            return render_template('admin_question.html', questions=questions, message=login_massage)

# 用户信息管理页面
@bp.route('/info', methods=["POST", "GET"])
@admin_required
def admin_info():
    if request.method == "GET":
        username = g.user
        info = dict()
        info['username'] = username
        info['password'] = get_user_content(username, password=True)
        return render_template("admin_info.html", info=info)
    else:
        username = request.form['username']
        password = request.form['password']

        if is_null(password):
            login_massage = "温馨提示：密码不能为空！"
            return render_template('admin_question.html', message=login_massage)
        else:
            info = dict()
            change_user_content(username, password=password)

            info['username'] = username
            info['password'] = get_user_content(username, password=True)[0]
            if check_password_hash(info['password'], password):
                login_massage = "温馨提示：密码修改成功！"
                info['password'] = password
            else:
                login_massage = "温馨提示：密码修改失败！"

            return render_template("admin_info.html", info=info, message=login_massage)

# 用户信息管理页面
@bp.route('/visual', methods=["POST", "GET"])
@admin_required
def admin_visual():
    if request.method == "GET":
        return render_template("admin_visual.html")