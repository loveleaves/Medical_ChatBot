# -*- coding: utf-8 -*-
import base64
import io
import random
import string
from PIL import Image, ImageFont, ImageDraw
from flask import session, Blueprint, render_template, request, url_for

from decorators import login_required
from utils.csv_utils import QuestionForm, get_all_user_content, change_user_content
from utils.visual_utils import generate_word_cloud

bp = Blueprint('api', __name__, url_prefix='/api')

class CaptchaTool(object):
    """
    生成图片验证码
    """
    def __init__(self, width=50, height=12):

        self.width = width
        self.height = height
        # 新图片对象
        self.im = Image.new('RGB', (width, height), 'white')
        # 字体
        self.font = ImageFont.load_default()
        # draw对象
        self.draw = ImageDraw.Draw(self.im)

    def draw_lines(self, num=3):
        """
        划线
        """
        for num in range(num):
            x1 = random.randint(0, self.width / 2)
            y1 = random.randint(0, self.height / 2)
            x2 = random.randint(0, self.width)
            y2 = random.randint(self.height / 2, self.height)
            self.draw.line(((x1, y1), (x2, y2)), fill='black', width=1)

    def get_verify_code(self):
        """
        生成验证码图形
        """
        # 设置随机4位数字验证码
        code = ''.join(random.sample(string.digits, 4))
        # 绘制字符串
        for item in range(4):
            self.draw.text((6 + random.randint(-3, 3) + 10 * item, 2 + random.randint(-2, 2)),
                        text=code[item],
                        fill=(random.randint(32, 127),
                                random.randint(32, 127),
                                random.randint(32, 127))
                        , font=self.font)
        # 划线
        # self.draw_lines()
        # 重新设置图片大小
        self.im = self.im.resize((100, 24))  
        # 图片转为base64字符串
        buffered = io.BytesIO()
        self.im.save(buffered, format="JPEG")
        img_str = "data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode()
        return img_str, code

@bp.route('/GetCaptcha', methods=["GET"])
def get_captcha():
    """
    function : 获取图形验证码
    :return: str
    """
    new_captcha = CaptchaTool()
    # 获取图形验证码
    img, code = new_captcha.get_verify_code()
    # 存入session
    session["code"] = code
    return img

@bp.route('/DelUser', methods=["GET"])
@login_required
def del_user():
    """
    function ： 在html中删除用户
    """
    user = request.args.get("user")
    change_user_content(user.strip(), del_user=True)
    all_user_info = get_all_user_content()
    return render_template("admin_user.html", users=all_user_info, message="删除成功！")

@bp.route('/DelQuestion', methods=["GET"])
@login_required
def del_question():
    """
    function ： 在html中删除用户问题
    """
    user = request.args.get("user")
    title = request.args.get("title")
    Form = QuestionForm(user)
    flag = Form.del_question(title)

    qustions = Form.get_all_question()
    if flag:
        message = "删除成功！"
    else:
        message = "删除失败！"
    return render_template("admin_question.html", qustions=qustions, message=message)

@bp.route('/GetUsername', methods=["GET"])
@login_required
def get_username():
    """
    function ： 在html中获取用户名
    :return: str
    """
    user = session.get("user_id")
    return user

@bp.route('/GetUserQuestion', methods=["GET"])
@login_required
def get_user_question():
    """
    function ： 获取用户所提问题
    """
    Form = QuestionForm()
    questions = Form.get_all_question()
    return questions

@bp.route('/GetAnswer', methods=["GET"])
@login_required
def get_answer():
    """
    function ： 获取对用户所提问题的回答
    :return: str
    """
    user = session.get("user_id")
    return user

# @bp.route("/email")
# def get_email_captcha():
#     """
#     function : 利用qq邮箱发送验证码
#     """
    # /captcha/email/<email>
    # /captcha/email?email=xxx
    email = request.args.get('email')
#     # 4 位： 顺机产生4个数值,字母，数值
#     source = string.digits * 4
#     captcha = "".join(random.sample(source, 4))
#     # IO操作，INPUT /OUTPUT
#     app = current_app._get_current_object()
#     message = Message(subject="乘风平台验证码", sender='3063254779@qq.com', recipients=[email],
#                       body=f"您的验证码是: {captcha}")
#     thread = Thread(target=send_async_email, args=[app, message])
#     thread.start()
#     # mail.send(message)
#
#     log.info("Sent email: {} and  captcha : {} ".format(email, captcha))
#     emailcaptcha = EmailCaptchaModel(email=email, captcha=captcha)
#     db.session.add(emailcaptcha)
#     db.session.commit()
#     # 使用数据库存储
#     # Restful API
#     # {'code': '200', 'message': '请求成功'}
#     return jsonify({'code': 200, 'message': '请求成功'})

@bp.route('/GetVisual', methods=["GET"])
@login_required
def get_visual():
    """
    function ： 获取可视化图片
    """
    img_base64 = generate_word_cloud()
    return "data:image/png;base64," + img_base64

if __name__ == "__main__":
    pass
