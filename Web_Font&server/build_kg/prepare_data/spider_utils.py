# -*- coding:utf-8 -*-
import os
import re
import json
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
from tqdm import tqdm
import threading
import requests
import time
import queue


def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/51.0.2704.63 Safari/537.36'}
    req = urllib.request.Request(url=url, headers=headers)
    res = urllib.request.urlopen(req)
    html = res.read().decode('gbk', errors='ignore')
    return html


def fqa_detail_parser(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    faq_info_tag = soup.find(attrs={"class": "fl w880"})
    faq_info_tag.prettify()
    qdetail = faq_info_tag.find(attrs={"class": "details-con clearfix"})
    qdetail = qdetail.get_text().strip()

    adetail_list = []
    ans_list = faq_info_tag.find_all(attrs={"class": "replay-content-box clearfix"})
    for ans_content in ans_list:
        adetail_list.append(str(ans_content.get_text().strip()))  # Tag -> str 格式
    return {'qdetail': str(qdetail), 'adetail_list': adetail_list}


def main_parser(html):
    soup = BeautifulSoup(html, 'html.parser')
    symptom = soup.find(attrs={"class": "jb-name fYaHei gre"})
    symptom_name = symptom.get_text()

    jieshao = soup.find(name='div', attrs={"class": "zz-articl fr f14"})
    jieshao_value = jieshao.get_text()
    jieshao_value = [jv.strip() for jv in jieshao_value.split('\n') if len(jv) > 10]
    jieshao_value = jieshao_value[0]

    xiangguan_zz_tag = soup.find(attrs={"class": "other-zz mt10"})
    xiangguan_zz_list = [xg_sym.get_text() for xg_sym in xiangguan_zz_tag.find_all('li')]

    faq_tag_list = soup.find_all(attrs={"class": "fl replay-note"})
    question_info_list = []
    ques_text_set = set()
    for faq in faq_tag_list:
        faq = faq.find('a')
        href = faq.get('href')
        ques_text = faq.get_text()
        if ques_text in ques_text_set:
            continue
        fqa_detail = fqa_detail_parser(href)
        question_info_list.append(
            {
                'text': ques_text,
                'href': href,
                'fqa_detail': fqa_detail
            }
        )
        ques_text_set.add(ques_text)

    return symptom_name, jieshao_value, xiangguan_zz_list, question_info_list


def attributes_parser(html):
    soup = BeautifulSoup(html, 'html.parser')
    attribute_tag = soup.find(name='div', attrs={"class": "zz-articl fr f14"})
    attribute = attribute_tag.get_text()
    attribute = re.sub(r'[\r\t]+', '\n', attribute)
    attribute = re.sub(r'[\n]+', '\n', attribute)
    return attribute.strip()


def food_parser(html):
    food_infos = {}
    soup = BeautifulSoup(html, 'html.parser')
    match_food_tag = soup.find(attrs={"class": "diet-item clearfix"})
    match_food = match_food_tag.find(attrs={"class": "fl diet-good-txt"})
    food_infos['match_food'] = {
        'describe': match_food.get_text(),
        'food_list': []
    }
    match_food_list = match_food_tag.find_all(attrs={"class": "diet-imgbox pr bor fl mr10"})
    for food in match_food_list:
        food_name = food.find(attrs={"class": "diet-opac-txt pa f12"})
        food_name = food_name.get_text()
        food_url = food.a.get('href')
        food_infos['match_food']['food_list'].append({'name': food_name, 'url': food_url})

    not_match_food_tag = soup.find(attrs={"class": "diet-item none"})
    not_match_food = not_match_food_tag.find(attrs={"class": "fl diet-good-txt"})
    food_infos['not_match_food'] = {
        'describe': not_match_food.get_text(),
        'food_list': []
    }
    not_match_food_list = not_match_food_tag.find_all(attrs={"class": "diet-imgbox pr bor fl mr10"})
    for food in not_match_food_list:
        food_name = food.find(attrs={"class": "diet-opac-txt pa f12"})
        food_name = food_name.get_text()
        food_url = food.a.get('href')
        food_infos['not_match_food']['food_list'].append({'name': food_name, 'url': food_url})
    return food_infos


def dump_json(symptom_tuple, all_attr_value_list, food_infos):
    symptom_name, jieshao_value, xiangguan_zz_list, question_info_list = symptom_tuple
    data_format = {
        "name": symptom_name,
        "jieshao": jieshao_value,
        "xiangguan_zz": xiangguan_zz_list,
        "question_infos": question_info_list,
        "food": food_infos
    }
    for item in all_attr_value_list:
        # print(item)
        data_format.update(item)

    # print(json.dumps(data_format, sort_keys=True, indent=4, separators=(', ', ': '),ensure_ascii=False))

    with open('symptom_data.json', 'a+', encoding='utf8') as f:
        f.write(json.dumps(data_format, ensure_ascii=False))
        f.write('\n')


# 为线程定义一个函数
class myThread(threading.Thread):
    def __init__(self, name, q):
        threading.Thread.__init__(self)
        self.name = name
        self.q = q

    def run(self):
        print("Starting " + self.name)
        while True:
            try:
                crawl(self.name, self.q)
            except:
                break
        print("Exiting " + self.name)


def crawl(q):
    base_url = 'https://zzk.xywy.com/{page}_{attr}.html'
    attri_list = ['yuanyin', 'yufang', 'jiancha', 'zhenduan']
    page = q.get(timeout=2)
    try:
        all_attr_value_list = []
        for attr in attri_list:
            url = base_url.format(page=str(page), attr=attr)
            # print(url)
            html = get_html(url)
            attr_value = attributes_parser(html)
            all_attr_value_list.append({attr: attr_value})

        url = base_url.format(page=str(page), attr='jieshao')
        html = get_html(url)
        symptom_tuple = main_parser(html)

        url = base_url.format(page=str(page), attr='food')
        html = get_html(url)
        food_infos = food_parser(html)

        dump_json(symptom_tuple, all_attr_value_list, food_infos)
    except Exception as e:
        print(e)
        print(url)


def run(num_page):
    URLs = [page for page in range(78, num_page)]

    # 填充队列
    workQueue = queue.Queue(len(URLs))
    for url in URLs:
        workQueue.put(url)

    threads = []
    # 多线程爬取
    for i in range(1, 161):
        # 创建160个新线程
        thread = myThread("Thread-" + str(i), q=workQueue)
        # 开启新线程
        thread.start()
        # 添加新线程到线程列表
        threads.append(thread)

    # 等待所有线程完成
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    run(11000)
