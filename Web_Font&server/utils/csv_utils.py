# -*- coding:utf-8 -*-
import csv
import pandas as pd
import os
import re
from werkzeug.security import check_password_hash, generate_password_hash

DB_DIR = "./db"
USER_FILE = 'user'
QUESTION_FILE = 'question'
CHATBOTQUESTION_FILE = 'chat_bot_question'
USER_IP_FILE = "user_ipaddress"
IP_NUM_FILE = "ip_usernums"

# DB默认配置文件
config = {
    'admin_name': 'admin',
    'admin_password': '123456',
    'password_input_times': 5,
    'chat_gpt_use_times': 10,
    'max': -3,
    'ip_reg_max_num': 50
}


class LoginUserInfo:
    """
    function: 登陆用户信息的管理
    """

    def __init__(self):
        self.user_ip_path = os.path.join(DB_DIR, '{}.csv'.format(USER_IP_FILE))
        self.ip_num_path = os.path.join(DB_DIR, '{}.csv'.format(IP_NUM_FILE))

    def check_malicious_registration(self, ip: str) -> bool:
        """
        function: 计算某ip范围内注册账户数量，用于防止恶意注册（也可用邮箱或手机号注册方式防止）
                可对某ip范围内注册账户数量进行限制（现阶段永久限制，可增加过多久才能注册， TODO）
        """
        # 计算策略：没采用子网划分的方法进行对比，这里直接比较后16位
        ip_arr = ip.split('.')
        assert len(ip_arr) == 4, "IP地址有问题！"
        # 以17-24位划分10组为同一类
        ip_arr[2] = str(int(int(ip_arr[2]) / 25))
        ip_arr[3] = "0"
        target_ip = '.'.join(ip_arr)
        ip_num = self.get_ip_num(target_ip) + 1
        if ip_num <= config['ip_reg_max_num']:
            return False
        else:
            return True

    def update_ip_num(self, ip: str, num=1):
        """
        function: 更新某ip范围内注册数量
        """
        path = self.ip_num_path

        if not os.path.exists(path):
            data = {'ip': [ip], 'num': [str(num)]}
            df = pd.DataFrame(data)
            df.to_csv(path, index=False)

        else:
            # 指定dtype，不然pandas自动数据转换
            df = pd.read_csv(path, dtype={"ip": str, "num": str})
            df.set_index('ip', inplace=True)

            ip_arr = ip.split('.')
            assert len(ip_arr) == 4, "IP地址有问题！"
            # 以17-24位划分10组为同一类
            ip_arr[2] = str(int(int(ip_arr[2]) / 25))
            ip_arr[3] = "0"
            target_ip = '.'.join(ip_arr)
            try:
                df.loc[target_ip.strip(), 'num'] = str(int(df.loc[target_ip.strip(), 'num']) + num)
                df.reset_index()
                df.to_csv(path)
            except:
                with open(path, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([target_ip.strip(), str(num)])

    def get_ip_num(self, ip: str):
        """
        function: 获取某ip范围内注册数量
        """
        path = self.ip_num_path
        assert os.path.exists(path)

        # 指定dtype，不然pandas自动数据转换
        df = pd.read_csv(path, dtype={"ip": str, "num": int})
        df.set_index('ip', inplace=True)

        try:
            return int(df.loc[ip.strip(), 'num'])
        except:
            return 0

    def add_user_reg_ip(self, username: str, ip: str):
        """
        function: 记录注册用户ip，可用于防止恶意注册（也可用邮箱或手机号注册方式防止），
            也可用于用户登陆安全校验（异地登陆等）
        """
        path = self.user_ip_path

        if not os.path.exists(path):
            data = {'username': [username], 'ip': [ip]}
            df = pd.DataFrame(data)
            df.to_csv(path, index=False)

        else:
            with open(path, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([username.strip(), ip.strip()])

    def update_user_ip(self, username: str, ip: str):
        """
        function: 仅保留最近一个ip
        """
        path = self.user_ip_path
        assert os.path.exists(path)

        # 指定dtype，不然pandas自动数据转换
        df = pd.read_csv(path, dtype={"username": str, "ip": str})
        df.set_index('username', inplace=True)

        try:
            df.loc[username.strip(), 'ip'] = ip
        except:
            self.add_user_reg_ip(username, ip)

        df.reset_index()
        df.to_csv(path)

    def get_user_ip(self, username: str):
        """
        function: 获取用户最近登陆ip（仅保留最近一个ip）
        """
        path = self.user_ip_path
        assert os.path.exists(path)

        # 指定dtype，不然pandas自动数据转换
        df = pd.read_csv(path, dtype={"username": str, "ip": str})
        df.set_index('username', inplace=True)

        try:
            return df.loc[username.strip(), 'ip']
        except:
            return None


def is_null(*args) -> bool:
    """
    function : 判断字符串参数是否为空
    """
    for item in args:
        if item.strip() == '':
            return True

    return False


def add_user(username: str, password: str):
    path = os.path.join(DB_DIR, '{}.csv'.format(USER_FILE))
    if not os.path.exists(path):
        data = {'username': [config['admin_name']], 'password': [generate_password_hash(config['admin_password'])],
                'PIT': [config['password_input_times']], 'CGUT': config['max']}
        df = pd.DataFrame(data)
        df.to_csv(path, index=False)
    else:
        with open(path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([username.strip(), password.strip(),
                             config['password_input_times'], config['chat_gpt_use_times']])


def get_all_user_content(include_admin=False) -> list:
    """
    function : get all the information of users.
    """
    path = os.path.join(DB_DIR, '{}.csv'.format(USER_FILE))
    assert os.path.exists(path), "用户配置文件丢失！"

    df = pd.read_csv(path, dtype={"username": str, "password": str, "PIT": int, "CGUT": int})
    all_user_info = []
    for i in range(len(df)):
        user_info = {}
        if not include_admin and df.iloc[i][0] == config['admin_name']:
            continue
        user_info['username'] = df.iloc[i][0]
        user_info['password'] = df.iloc[i][1]
        user_info['PIT'] = df.iloc[i][2]
        user_info['CGUT'] = df.iloc[i][3]
        all_user_info.append(user_info)

    return all_user_info


def get_user_content(username: str, password=False, password_input_times=False, chat_gpt_use_times=False):
    """
    function : get user information
    return : ["password":str,"PIT":int,"CGUT":int]
    """
    path = os.path.join(DB_DIR, '{}.csv'.format(USER_FILE))
    assert os.path.exists(path), "用户配置文件丢失！"

    df = pd.read_csv(path, dtype={"username": str, "password": str, "PIT": int, "CGUT": int})
    df.set_index('username', inplace=True)
    if isinstance(username, list):
        user_info = []
        for user in username:
            ans = df.loc[user.strip()]
            tmp = []
            if password:
                tmp.append(ans.password)
            if password_input_times:
                tmp.append(ans.PIT)
            if chat_gpt_use_times:
                tmp.append(ans.CGUT)
            user_info.append(tmp)
        return user_info
    else:
        ans = df.loc[username.strip()]
        user_info = []
        if password:
            user_info.append(ans.password)
        if password_input_times:
            user_info.append(ans.PIT)
        if chat_gpt_use_times:
            user_info.append(ans.CGUT)
        return user_info


def change_user_content(username, password="", password_input_times="", chat_gpt_use_times="", **kwargs):
    """
    function : change user information
    input : must be str, but store in other type
    """
    path = os.path.join(DB_DIR, '{}.csv'.format(USER_FILE))
    assert isinstance(password, str), "密码必须为字符串"
    if len(password) < 50:
        password = generate_password_hash(password)
    assert isinstance(password_input_times, str), "PIT必须为字符串"
    assert isinstance(chat_gpt_use_times, str), "CGUT必须为字符串"
    assert os.path.exists(path), "用户配置文件丢失！"

    # 指定dtype，不然pandas自动数据转换
    df = pd.read_csv(path, dtype={"username": str, "password": str, "PIT": int, "CGUT": int})
    df.set_index('username', inplace=True)

    if isinstance(username, list):
        # 以下采取全部赋同一值的策略
        for user in username:
            ans = df.loc[user.strip()]
            if password:
                df.loc[user.strip(), 'password'] = password
            if password_input_times:
                tmp = int(ans.PIT)
                if password_input_times != '-1':
                    df.loc[user.strip(), 'PIT'] = int(password_input_times)
                else:
                    df.loc[user.strip(), 'PIT'] = tmp - 1
            if chat_gpt_use_times and ans.CGUT != config['max']:
                tmp = int(ans.CGUT)
                if chat_gpt_use_times != '-1':
                    df.loc[user.strip(), 'CGUT'] = int(chat_gpt_use_times)
                else:
                    df.loc[user.strip(), 'CGUT'] = tmp - 1
    else:
        try:
            ans = df.loc[username.strip()]
            if password:
                df.loc[username.strip(), 'password'] = password
            if password_input_times:
                tmp = int(ans.PIT)
                if password_input_times != '-1':
                    df.loc[username.strip(), 'PIT'] = int(password_input_times)
                else:
                    df.loc[username.strip(), 'PIT'] = tmp - 1
            if chat_gpt_use_times and ans.CGUT != config['max']:
                tmp = int(ans.CGUT)
                if chat_gpt_use_times != '-1':
                    df.loc[username.strip(), 'CGUT'] = int(chat_gpt_use_times)
                else:
                    df.loc[username.strip(), 'CGUT'] = tmp - 1
            if 'del_user' in kwargs and kwargs['del_user']:
                df = df.drop(username.strip(), axis=0)
        except:
            pass

    df.reset_index()
    df.to_csv(path)


def passwd_comp(username: str, password: str):
    """
    function : check whether the password is correct
    return : (int : password_input_times, bool : flag)
    """
    path = os.path.join(DB_DIR, '{}.csv'.format(USER_FILE))
    assert os.path.exists(path), "用户配置文件丢失！"

    ans = get_user_content(username, password=True, password_input_times=True)
    if check_password_hash(ans[0], password.strip()):
        return (ans[1], True)
    else:
        if ans[1] > 0:
            change_user_content(username, password_input_times="-1")
            return (ans[1] - 1, False)
        else:
            return (0, False)


def is_existed(username):
    """
    function : check whether the user exists
    Note : 不能用get_user_content()函数代替，因为其默认用户存在，否则报错
    """
    path = os.path.join(DB_DIR, '{}.csv'.format(USER_FILE))
    assert isinstance(username, str), "用户名必须为字符串"
    assert os.path.exists(path), "用户配置文件丢失！"

    df = pd.read_csv(path)
    df.set_index('username', inplace=True)
    try:
        ans = df.loc[username.strip()]
        return True
    except:
        return False


def check_passwd(password):
    """
    function : check whether the password meets the requirements
    """
    assert isinstance(password, str), "密码必须为字符串"
    password = password.strip()
    # print(password)
    if len(password) < 6 or len(password) > 20:
        return (False, "密码长度必须 6-20之间")
    elif re.match("^(?:(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])).*$", password) == None:
        return (False, "密码必须包含大小写字母和数字")
    else:
        return (True, "密码符合要求")


class ChatBotQuestion:
    """
    function : 管理用户询问问题中的实体、意图等用于可视化分析
    """

    def __init__(self):
        self.path = os.path.join(DB_DIR, '{}.csv'.format(CHATBOTQUESTION_FILE))

    def store_question_entity(self, **kwargs) -> bool:
        """
        function : 存储用户询问问题中的实体
        """
        username = kwargs['username']
        entity_type = kwargs['entity_type'].strip()
        entity_name = kwargs['entity_name'].strip()

        if not os.path.exists(self.path):
            data = {'username': [username], 'entity_type': [entity_type], 'entity_name': [entity_name]}
            df = pd.DataFrame(data)
            df.to_csv(self.path, index=False)
            return True
        else:
            with open(self.path, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([username, entity_type, entity_name])
            return True

    def get_all_entity(self, include_username=False):
        """
        function : get all the entities
        """
        entities = []

        df = pd.read_csv(self.path, dtype={"username": str, "entity_type": str, 'entity_name': str})
        for index in range(len(df)):
            entity = []
            if include_username:
                entity.append(df.iloc[index, 0])
            entity.append(df.iloc[index, 1])
            entity.append(df.iloc[index, 2])

            entities.append(entity)

        return entities


class QuestionForm:
    """
    function : 问题判断处理类
    """

    def __init__(self, user):
        self.user = user

    def get_all_question(self):
        """
        function : 获取所有用户问题
        return : [{'user':'a','title':'da','question':'d','answer':'a'},]
        """
        path = os.path.join(DB_DIR, '{}.csv'.format(QUESTION_FILE))
        assert os.path.exists(path), "用户配置文件丢失！"

        df = pd.read_csv(path, dtype={"user": str, "title": str, 'question': str, "answer": str})
        ans = df.values.tolist()
        questions = []

        for question in ans:
            question_info = dict()
            question_info['username'] = question[0]
            question_info['title'] = question[1]
            question_info['question'] = question[2]
            question_info['answer'] = question[3]

            questions.append(question_info)

        return questions

    def del_question(self, title) -> bool:
        """
        function : del the questions from users.
        """
        path = os.path.join(DB_DIR, '{}.csv'.format(QUESTION_FILE))
        assert os.path.exists(path), "用户配置文件丢失！"

        df = pd.read_csv(path, dtype={"user": str, "title": str, 'question': str, "answer": str})
        try:
            for i in range(len(df)):
                if str(df.iloc[i][0]).strip() == self.user:
                    if str(df.iloc[i][1]) == title:
                        df = df.drop([i], axis=0)

                        df.to_csv(path, index=False)
                        return True
        except:
            pass

        return False

    def update_answer(self, title: str, answer: str, **kwargs) -> bool:
        """
        function : update the contents of question by admin.
        """
        path = os.path.join(DB_DIR, '{}.csv'.format(QUESTION_FILE))
        assert os.path.exists(path), "用户配置文件丢失！"

        df = pd.read_csv(path, dtype={"user": str, "title": str, 'question': str, "answer": str})
        for i in range(len(df)):
            if str(df.iloc[i][0]).strip() == self.user:
                if str(df.iloc[i][1]) == title:
                    df.iloc[i][3] = answer.strip()
                    if 'question' in kwargs and kwargs['question']:
                        df.iloc[i][2] = kwargs['question'].strip()

                    if 'previous_title' in kwargs and kwargs['previous_title']:
                        df.iloc[i][1] = kwargs['previous_title'].strip()

                    df.to_csv(path, index=False)
                    return True

        return False

    def store_question(self, title: str, question: str) -> str:
        """
        function : store the questions from users.
        """
        title = title.strip()
        question = question.strip()
        if is_null(title, question):
            return "问题和标题不能为空!"
        if len(question) > 300 or len(title) > 30:
            return "输入文字过多!"

        path = os.path.join(DB_DIR, '{}.csv'.format(QUESTION_FILE))
        if not os.path.exists(path):
            data = {'user': [self.user.strip()], 'title': [title], 'question': [question], 'answer': [" "]}
            df = pd.DataFrame(data)
            df.to_csv(path, index=False)
            return "问题提交成功!"
        else:
            # 只不允许重复标题title
            questions = [i[0] for i in self.get_user_question()]
            if question in questions:
                return "请勿重复提交问题!"
            with open(path, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([self.user.strip(), title, question, " "])
        return "问题提交成功!"

    def get_user_question(self) -> list:
        # return : [(title, question),]
        path = os.path.join(DB_DIR, '{}.csv'.format(QUESTION_FILE))
        assert os.path.exists(path), "用户配置文件丢失！"

        df = pd.read_csv(path, dtype={"user": str, "title": str, "question": str, 'answer': str})
        questions = []
        try:
            df.set_index('user', inplace=True)
            ans = df.loc[self.user]
            ans = ans.values.tolist()

            for question in ans:
                if isinstance(question, list):
                    questions.append((question[0], question[1], question[2].strip()))
                else:
                    questions.append((ans[0], ans[1], ans[2].strip()))
                    break
            return questions
        except:
            return []


if __name__ == "__main__":
    # 如果用户配置文件丢失，请运行此主函数
    DB_DIR = "../db"
    # add_user('a', 'a')
    user_info_manager = LoginUserInfo()
    # user_info_manager.update_ip_num("127.0.1.0")
    user_info_manager.add_user_reg_ip("admin", "127.0.0.1")
