# -*- coding:utf-8 -*-
import sys
import uuid
import requests
import hashlib
import time
from imp import reload

reload(sys)

from asr_tts.config import youdao_api


class YouDaoTTSAPI:
    def __init__(self):
        self.YOUDAO_URL = 'https://openapi.youdao.com/ttsapi'

    def encrypt(self, signStr):
        hash_algorithm = hashlib.md5()
        hash_algorithm.update(signStr.encode('utf-8'))
        return hash_algorithm.hexdigest()

    def truncate(self, q):
        if q is None:
            return None
        size = len(q)
        return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]

    def do_request(self, data):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return requests.post(self.YOUDAO_URL, data=data, headers=headers)

    def tts(self, q: str, langType='zh-CHS', tts_file_path="tts.mp3"):
        """
        function: TTS
        langType:
            普通话（中国台湾）:zh-TWN
            粤语:yue（只支持女声）
            英语（美国）:en-USA
        """
        data = {}
        data['langType'] = langType
        salt = str(uuid.uuid1())
        signStr = youdao_api['APP_KEY'] + q + salt + youdao_api['APP_SECRET']
        sign = self.encrypt(signStr)
        data['appKey'] = youdao_api['APP_KEY']
        data['q'] = q
        data['salt'] = salt
        data['sign'] = sign

        response = self.do_request(data)
        contentType = response.headers['Content-Type']
        if contentType == "audio/mp3":
            print(response.content)
            with open(tts_file_path, 'wb') as f:
                f.write(response.content)
            return True
        else:
            print(response.content)
            return False


if __name__ == "__main__":
    youdao_tts = YouDaoTTSAPI()
    youdao_tts.tts("你好")
