import collections
import re
import jieba
import cv2
import base64
import numpy as np
from pyecharts.charts import Bar
from pyecharts.globals import ThemeType
import pyecharts.options as opts
from wordcloud import WordCloud
from PIL import Image
from matplotlib import pyplot as plt
from io import BytesIO
from collections import defaultdict

from utils.csv_utils import ChatBotQuestion

WORK_DIR = "./utils/"
style_pic_path = WORK_DIR + 'wc.jpg'


def words_counts():
    with open('test.txt', mode='r', encoding='utf-8') as f:
        strData = f.read()

    # 替换符合parrtern的文本
    pattern = re.compile(r'\t|,|/|。|\n|\.|-|:|;|\)|\(|\?|，。，！”"')
    strData = re.sub(pattern, '', strData)  # 将符合模式的字符去除

    # 开始分词，精准模式
    words = jieba.cut(strData, cut_all=False)
    resultWords = []  # 空列表
    # 自定义停用词
    stopWords = [u'的', u'要', u'“', u'”', u'和', u'，', u'为', u'是',
                 '以' u'随着', u'对于', u'对', u'等', u'能', u'都', u'。',
                 u' ', u'、', u'中', u'在', u'了', u'通常', u'如果', u'我',
                 u'她', u'（', u'）', u'他', u'你', u'？', u'—', u'就',
                 u'着', u'说', u'上', u'这', u'那', u'有', u'也',
                 u'什么', u'·', u'将', u'没有', u'到', u'不', u'去']
    #
    for word in words:
        if word not in stopWords:
            resultWords.append(word)
    # print(resultWords) #  打印结果

    # 开始统计词频
    word_counts = collections.Counter(resultWords)  # 一个词频统计对象
    # print(word_counts)

    # 获取高频词的列表
    word_counts_all = word_counts.most_common()  # 一个列表，列表里是元组
    # print(word_counts_all)
    word_counts_top10 = word_counts.most_common(10)
    return word_counts_top10


def word_cloud_style():
    """
    function : 从文件生成词云
    """
    with open('test.txt', mode='r', encoding='utf-8') as f:
        txt = f.read()
    # 如果是文章的话，需要用到jieba分词，分完之后也可以自己处理下再生成词云
    newTxt = re.sub("A-Z0-9-a-z\!\%\[\]\,\。", "", txt)

    words = jieba.lcut(newTxt)
    # print(words)
    img = Image.open(r'wc.jpg')  # 想要做的形状
    img_array = np.array(img)

    # 相关配置，里面这个collections可以避免重复
    wordcloud = WordCloud(
        background_color='white',
        width=1080,
        height=960,
        font_path='SimHei.ttf',
        max_words=150,
        scale=10,  # 清晰度
        max_font_size=100,
        mask=img_array,
        collocations=False).generate(newTxt)

    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()
    wordcloud.to_file('wc.png')


class DataTypeConvert:
    def img_to_base64(self, img_array):
        # 传入图片为RGB格式numpy矩阵，传出的base64也是通过RGB的编码
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)  # RGB2BGR，用于cv2编码
        encode_image = cv2.imencode(".jpg", img_array)[1]  # 用cv2压缩/编码，转为一维数组
        byte_data = encode_image.tobytes()  # 转换为二进制
        base64_str = base64.b64encode(byte_data).decode("ascii")  # 转换为base64
        return base64_str

    def base64_to_img(self, base64_str):
        # 传入为RGB格式下的base64，传出为RGB格式的numpy矩阵
        byte_data = base64.b64decode(base64_str)  # 将base64转换为二进制
        encode_image = np.asarray(bytearray(byte_data), dtype="uint8")  # 二进制转换为一维数组
        img_array = cv2.imdecode(encode_image, cv2.IMREAD_COLOR)  # 用cv2解码为三通道矩阵
        img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)  # BGR2RGB
        return img_array

    def image_to_base64(self, image):
        # 输入为PIL读取的图片，输出为base64格式
        byte_data = BytesIO()  # 创建一个字节流管道
        image.save(byte_data, format="JPEG")  # 将图片数据存入字节流管道
        byte_data = byte_data.getvalue()  # 从字节流管道中获取二进制
        base64_str = base64.b64encode(byte_data).decode("ascii")  # 二进制转base64
        return base64_str

    def base64_to_image(self, base64_str):
        # 输入为base64格式字符串，输出为PIL格式图片
        byte_data = base64.b64decode(base64_str)  # base64转二进制
        image = Image.open(BytesIO(byte_data))  # 将二进制转为PIL格式图片
        return image


def generate_word_cloud():
    form = ChatBotQuestion()
    entities = form.get_all_entity()
    ans = ""
    for entity in entities:
        ans += "," + ','.join(entity)

    img = Image.open(style_pic_path)  # 想要做的形状
    img_array = np.array(img)

    # 相关配置，里面这个collections可以避免重复
    wordcloud = WordCloud(
        background_color='white',
        width=1080,
        height=960,
        font_path=WORK_DIR + 'SimHei.ttf',
        max_words=150,
        scale=10,  # 清晰度
        max_font_size=100,
        mask=img_array,
        collocations=False).generate(ans)

    arr = wordcloud.to_image()
    # arr = wordcloud.to_array()
    data_converter = DataTypeConvert()
    img_base64 = data_converter.image_to_base64(arr)
    # print(type(img_base64))
    return img_base64


def echart_top_10():
    data = words_counts()
    lab = [i[0] for i in data]
    num = [i[1] for i in data]
    # print(lab, num)

    bar = (
        Bar(init_opts=opts.InitOpts(width='1000px', height='700px', theme=ThemeType.LIGHT))
        .add_xaxis(xaxis_data=lab)
        .add_yaxis(
            series_name='',
            y_axis=num,
            label_opts=opts.LabelOpts(is_show=True, color='red'),
            bar_max_width='100px',
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title='高词频前10',
                title_textstyle_opts=opts.TextStyleOpts(font_size=28, )
            ),
            legend_opts=opts.LegendOpts(
                pos_top='10%',
                pos_left='10%',
            ),
            xaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(rotate=45),  # 倾斜45度
            ),
            toolbox_opts=opts.ToolboxOpts(),
            tooltip_opts=opts.TooltipOpts(
                is_show=True,
                trigger='axis',  # 触发类型，(axis表示坐标轴触发，鼠标移动上去的时候会有一条垂直于x轴的实线跟随鼠标移动，并且提示信息)
                axis_pointer_type='cross',  # 指示器类型，(Cross表示生成两条分别垂直于x轴和y轴的虚线，不启用trigger才会显示完全)
            ),
        )
    ).render('top10.html')


class VisualData:
    def __init__(self):
        self.pic_path = "./visual_ans.png"

    def show_bar_image(self, x_data: list, y_data: list, x_label="x", y_label="y", title="柱状图", save_image=False,
                       save_image_path=""):
        """
        function: 显示并保存图片
        """
        font_dict = {'fname': './SimHei.ttf', 'size': 19}
        plt.rcParams["font.sans-serif"] = ['SimHei']
        plt.rcParams["axes.unicode_minus"] = False

        for i in range(len(x_data)):
            plt.bar(x_data[i], y_data[i])

        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)

        if save_image:
            if save_image_path:
                plt.savefig(save_image_path, font_dict=font_dict)
            else:
                plt.savefig(self.pic_path, font_dict=font_dict)

        plt.show(font_dict=font_dict)

    def show_maxlen(self, data: list, save_image_path=""):
        """
        function: 可视化数据中的长度分布
        """
        line_data = defaultdict(int)
        for item in data:
            line_data[len(item)] += 1

        xy_data = sorted(line_data.items(), key=lambda x: x[0])
        x = [i[0] for i in xy_data]
        y = [i[1] for i in xy_data]

        self.show_bar_image(x, y, x_label="长度", y_label="数量", title="数量分布图", save_image=True,
                            save_image_path=save_image_path)


if __name__ == "__main__":
    # generate_word_cloud()
    visualer = VisualData()
    visualer.show_bar_image([i for i in range(5)], [i for i in range(5)], x_label="长度", y_label="数量",
                            title="数量分布图", save_image=False)
