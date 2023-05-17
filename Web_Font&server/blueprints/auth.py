# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

from utils.csv_utils import is_null, is_existed, change_user_content, passwd_comp, config, check_passwd, add_user, \
    LoginUserInfo
from decorators import logout_required

bp = Blueprint("auth", __name__, url_prefix="/auth")


def wrong_captcha(code, get_wrong_message=False):
    # 获取session中的验证码
    s_code = session.get("code", None)
    # print(code, s_code)
    if not all([code, s_code]):
        if get_wrong_message:
            return "参数错误"
        else:
            return True
    if code != s_code:
        if get_wrong_message:
            return "验证码错误"
        else:
            return True
    return False


# 登陆页面
@bp.route("/user_login", methods=["POST", "GET"])
@logout_required
def user_login():
    if request.method == 'POST':  # 注册发送的请求为POST请求
        username = request.form['username']
        password = request.form['password']
        captcha = request.form['captcha']
        user_info_manager = LoginUserInfo()

        if is_null(username, password, captcha):
            login_massage = "温馨提示：账号、密码和验证码都不能为空"
            return render_template('login.html', message=login_massage)
        elif wrong_captcha(captcha):
            login_massage = wrong_captcha(captcha, get_wrong_message=True)
            return render_template('login.html', message=login_massage)
        elif not is_existed(username):
            login_massage = "温馨提示：不存在该用户，请先注册"
            return render_template('login.html', message=login_massage)
        else:
            password_input_times, flag = passwd_comp(username, password)
            if flag:
                # 其他信息全部正确，下面检验ip安全, TODO
                # recent_ip = user_info_manager.get_user_ip(username)
                now_ip = request.remote_addr
                # if recent_ip != now_ip:
                #     pass
                if password_input_times != config['password_input_times']:
                    change_user_content(username, password_input_times=str(config['password_input_times']))
                session['user_id'] = username
                user_info_manager.update_user_ip(username, now_ip)
                # flash(f"用户：{username} 登录成功")
                if username.strip() == config['admin_name'].strip():
                    return redirect(url_for("admin.admin_index"))
                else:
                    return redirect('/')
            else:
                if password_input_times > 0:
                    login_massage = f"温馨提示：密码错误，请输入正确密码，还剩{password_input_times}次机会。"
                    return render_template('login.html', message=login_massage)
                else:
                    login_massage = "温馨提示：密码错误次数过多，请联系管理员解决。"
                    return render_template('login.html', message=login_massage)
    else:
        return render_template('login.html')


@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# 注册页面
@bp.route("/user_register", methods=["GET", 'POST'])
@logout_required
def user_register():
    if request.method == 'POST':
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']
        captcha = request.form['captcha']
        user_info_manager = LoginUserInfo()
        if password1 != password2:
            login_massage = "两次密码不一致"
            return render_template('register.html', message=login_massage)
        elif is_null(username, password1, captcha):
            login_massage = "温馨提示：账号、密码和验证码都不能为空"
            return render_template('register.html', message=login_massage)
        elif wrong_captcha(captcha):
            login_massage = wrong_captcha(captcha, get_wrong_message=True)
            return render_template('register.html', message=login_massage)
        elif is_existed(username):
            login_massage = "温馨提示：用户已存在，请直接登录"
            # return redirect(url_for('user_login'))
            return render_template('register.html', message=login_massage)
        elif len(username) > 30:
            login_massage = "温馨提示：用户名太长"
            return render_template('register.html', message=login_massage)
        else:
            flag, login_massage = check_passwd(password1)
            if flag:
                # 以上信息全部正确，下面进行恶意账户注册检验
                user_ip = request.remote_addr
                if user_info_manager.check_malicious_registration(user_ip):
                    login_massage = "注册失败，系统检测到恶意注册！"
                    return render_template('register.html', message=login_massage)
                else:
                    # 用户密码采用hash加密存储
                    login_massage = "注册成功"
                    add_user(username, generate_password_hash(password1))
                    user_info_manager.add_user_reg_ip(username, user_ip)
                    user_info_manager.update_ip_num(user_ip)
                    return render_template('register.html', message=login_massage)
            else:
                return render_template('register.html', message=login_massage)
    return render_template('register.html')
