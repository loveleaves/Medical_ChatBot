# coding: utf-8
import json
import urllib.request
import urllib.parse
import threading
import queue
from lxml import etree


class myThread(threading.Thread):
    """
    function: 为线程定义一个函数
    """

    def __init__(self, name, q):
        threading.Thread.__init__(self)
        self.name = name
        self.q = q

    def run(self):
        print("Starting " + self.name)
        handler = CrimeSpider()
        while True:
            try:
                page = self.q.get(timeout=2)
                handler.spider_main(page)
            except:
                break
        print("Exiting " + self.name)


class CrimeSpider:
    def __init__(self):
        self.data_path = "./raw_data.json"
        self.db_path = "./db.json"

    def get_html(self, url):
        '''
        function: 根据url，请求html
        '''
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/51.0.2704.63 Safari/537.36'}
        req = urllib.request.Request(url=url, headers=headers)
        res = urllib.request.urlopen(req)
        html = res.read().decode('gbk')
        return html

    def url_parser(self, content):
        '''
        function: url解析
        '''
        selector = etree.HTML(content)
        urls = ['http://www.anliguan.com' + i for i in selector.xpath('//h2[@class="item-title"]/a/@href')]
        return urls

    def spider_main(self, page):
        '''
        function: 抓取主程序
        '''
        try:
            basic_url = 'http://jib.xywy.com/il_sii/gaishu/%s.htm' % page
            cause_url = 'http://jib.xywy.com/il_sii/cause/%s.htm' % page
            prevent_url = 'http://jib.xywy.com/il_sii/prevent/%s.htm' % page
            symptom_url = 'http://jib.xywy.com/il_sii/symptom/%s.htm' % page
            inspect_url = 'http://jib.xywy.com/il_sii/inspect/%s.htm' % page
            treat_url = 'http://jib.xywy.com/il_sii/treat/%s.htm' % page
            food_url = 'http://jib.xywy.com/il_sii/food/%s.htm' % page
            drug_url = 'http://jib.xywy.com/il_sii/drug/%s.htm' % page
            data = {}
            data['url'] = basic_url
            data['basic_info'] = self.basicinfo_spider(basic_url)
            data['cause_info'] = self.common_spider(cause_url)
            data['prevent_info'] = self.common_spider(prevent_url)
            data['symptom_info'] = self.symptom_spider(symptom_url)
            data['inspect_info'] = self.inspect_spider(inspect_url)
            data['treat_info'] = self.treat_spider(treat_url)
            data['food_info'] = self.food_spider(food_url)
            data['drug_info'] = self.drug_spider(drug_url)
            # print(page, basic_url)
            with open(self.data_path, "a", encoding='utf-8') as f:
                f.write(json.dumps(data, ensure_ascii=False))
                f.write("\n")

        except Exception as e:
            print(e, page)

    def basicinfo_spider(self, url):
        '''
        function: 基本信息解析
        '''
        html = self.get_html(url)
        selector = etree.HTML(html)
        title = selector.xpath('//title/text()')[0]
        category = selector.xpath('//div[@class="wrap mt10 nav-bar"]/a/text()')
        desc = selector.xpath('//div[@class="jib-articl-con jib-lh-articl"]/p/text()')
        ps = selector.xpath('//div[@class="mt20 articl-know"]/p')
        infobox = []
        for p in ps:
            info = p.xpath('string(.)').replace('\r', '').replace('\n', '') \
                .replace('\xa0', '').replace('   ', '').replace('\t', '')
            infobox.append(info)
        basic_data = {}
        basic_data['category'] = category
        basic_data['name'] = title.split('的简介')[0]
        basic_data['desc'] = desc
        basic_data['attributes'] = infobox
        return basic_data

    def treat_spider(self, url):
        '''
        function: treat_infobox治疗解析
        '''
        html = self.get_html(url)
        selector = etree.HTML(html)
        ps = selector.xpath('//div[starts-with(@class,"mt20 articl-know")]/p')
        infobox = []
        for p in ps:
            info = p.xpath('string(.)').replace('\r', '').replace('\n', ''). \
                replace('\xa0', '').replace('   ', '').replace('\t', '')
            infobox.append(info)
        return infobox

    def drug_spider(self, url):
        '''
        function: treat_infobox治疗解析
        '''
        html = self.get_html(url)
        selector = etree.HTML(html)
        drugs = [i.replace('\n', '').replace('\t', '').replace(' ', '') for i in
                 selector.xpath('//div[@class="fl drug-pic-rec mr30"]/p/a/text()')]
        return drugs

    def food_spider(self, url):
        '''
        function: food治疗解析
        '''
        html = self.get_html(url)
        selector = etree.HTML(html)
        divs = selector.xpath('//div[@class="diet-img clearfix mt20"]')
        try:
            food_data = {}
            food_data['good'] = divs[0].xpath('./div/p/text()')
            food_data['bad'] = divs[1].xpath('./div/p/text()')
            food_data['recommand'] = divs[2].xpath('./div/p/text()')
        except:
            return {}

        return food_data

    def symptom_spider(self, url):
        '''
        function: 症状信息解析
        '''
        html = self.get_html(url)
        selector = etree.HTML(html)
        symptoms = selector.xpath('//a[@class="gre" ]/text()')
        ps = selector.xpath('//p')
        detail = []
        for p in ps:
            info = p.xpath('string(.)').replace('\r', '').replace('\n', ''). \
                replace('\xa0', '').replace('   ', '').replace('\t', '')
            detail.append(info)
        symptoms_data = {}
        symptoms_data['symptoms'] = symptoms
        symptoms_data['symptoms_detail'] = detail
        return symptoms, detail

    def inspect_spider(self, url):
        '''
        function: 检查信息解析
        '''
        html = self.get_html(url)
        selector = etree.HTML(html)
        inspects = selector.xpath('//li[@class="check-item"]/a/@href')
        return inspects

    def common_spider(self, url):
        '''
        function: 通用解析模块
        '''
        html = self.get_html(url)
        selector = etree.HTML(html)
        ps = selector.xpath('//p')
        infobox = []
        for p in ps:
            info = p.xpath('string(.)').replace('\r', '').replace('\n', ''). \
                replace('\xa0', '').replace('   ', '').replace('\t', '')
            if info:
                infobox.append(info)
        return '\n'.join(infobox)

    def inspect_crawl(self):
        '''
        function: 检查项抓取模块
        '''
        for page in range(1, 3685):
            try:
                url = 'http://jck.xywy.com/jc_%s.html' % page
                html = self.get_html(url)
                data = {}
                data['url'] = url
                data['html'] = html
                with open(self.db_path, "a", encoding='utf-8') as f:
                    f.write(json.dumps(data, ensure_ascii=False))
                    f.write("\n")
                print(url)
            except Exception as e:
                print(e)


def crawl_main(num_page, thread_num=60):
    """
    function: 多线程爬取
    """
    URLs = [page for page in range(1, num_page)]

    # 填充队列
    workQueue = queue.Queue(len(URLs))
    for url in URLs:
        workQueue.put(url)

    threads = []
    for i in range(1, thread_num + 1):
        thread = myThread("Thread-" + str(i), q=workQueue)
        # 开启新线程
        thread.start()
        # 添加新线程到线程列表
        threads.append(thread)

    # 等待所有线程完成
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    crawl_main(11000, thread_num=60)
