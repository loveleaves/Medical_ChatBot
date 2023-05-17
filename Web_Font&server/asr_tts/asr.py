# -*- coding:utf-8 -*-
import os
# import whisper
import sys
import uuid
import requests
import wave
import base64
import hashlib
from imp import reload
import time

reload(sys)

from asr_tts.config import youdao_api


class YouDaoASRAPI:
    def __init__(self):
        self.YOUDAO_URL = 'https://openapi.youdao.com/asrapi'

    def truncate(self, q):
        if q is None:
            return None
        size = len(q)
        return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]

    def encrypt(self, signStr):
        hash_algorithm = hashlib.sha256()
        hash_algorithm.update(signStr.encode('utf-8'))
        return hash_algorithm.hexdigest()

    def do_request(self, data):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return requests.post(self.YOUDAO_URL, data=data, headers=headers)

    def audio_from_file(self, audio_file_path):
        """
        function: 从本地文件读取
        """
        assert os.path.exists((audio_file_path)), "本地音频文件缺失！"

        extension = audio_file_path[audio_file_path.rindex('.') + 1:]
        support_extension = ['wav']  # mp3等暂时不支持
        if extension not in support_extension:
            # 可利用ffmpeg转换格式，TODO
            print('不支持的音频类型')
            sys.exit(1)
        wav_info = wave.open(audio_file_path, 'rb')
        sample_rate = wav_info.getframerate()
        nchannels = wav_info.getnchannels()
        wav_info.close()
        # sample_rate = 16000
        # nchannels = 1
        with open(audio_file_path, 'rb') as file_wav:
            base64_str = base64.b64encode(file_wav.read()).decode('utf-8')

        return sample_rate, nchannels, base64_str

    def asr(self, audio_from_file=False, **kwargs):
        """
        function: ASR
        lang_type:
            普通话（中国台湾）:zh-TWN
            粤语:yue
            英语（美国）:en
        file_type:
            wav（不压缩，pcm编码，采样率：推荐16k ，编码：16bit位深的单声道）: wav
            aac: aac
            mp3: mp3
        params:
            audio_from_file=False, 需要sample_rate, nchannels, base64_str字段
            audio_from_file=True，需要audio_file_path字段
        """
        if audio_from_file:
            if 'audio_file_path' not in kwargs:
                assert False, "缺失字段：audio_file_path"
            audio_file_path = kwargs['audio_file_path']
            sample_rate, nchannels, base64_str = self.audio_from_file(audio_file_path)
        else:
            assert 'sample_rate' in kwargs and 'nchannels' in kwargs and 'base64_str' in kwargs, "缺少必要字段！"
            sample_rate, nchannels, base64_str = kwargs['sample_rate'], kwargs['nchannels'], kwargs['base64_str']
        lang_type = 'zh-CHS'

        data = {}
        curtime = str(int(time.time()))
        data['curtime'] = curtime
        salt = str(uuid.uuid1())
        signStr = youdao_api['APP_KEY'] + self.truncate(base64_str) + salt + curtime + youdao_api['APP_SECRET']
        sign = self.encrypt(signStr)
        data['appKey'] = youdao_api['APP_KEY']
        data['q'] = base64_str
        data['salt'] = salt
        data['sign'] = sign
        data['signType'] = "v2"
        data['langType'] = lang_type
        data['rate'] = sample_rate
        data['format'] = 'wav'
        data['channel'] = nchannels
        data['type'] = 1

        response = self.do_request(data)
        print(response.content)
        true = 1  # 用于下面防止转换出错，勿删
        false = 0
        try:
            ans = str(response.content, encoding='utf-8')
            ans_str = eval(ans)['result'][0]
        except Exception as e:
            print(e)
            ans_str = "语音识别返回结果错误！"

        return ans_str


# class WhisperModel:
#     def __init__(self):
#         self.model_name = "medium"
#
#     def ASR(self, file_path: str) -> str:
#         """
#         function: ASR
#         """
#         model = whisper.load_model(self.model_name)
#         result = model.transcribe(file_path)
#
#         text = []
#         for segment in result["segments"]:
#             text.append(segment["text"].strip())
#
#         return ','.join(text)


if __name__ == "__main__":
    youdao_asr = YouDaoASRAPI()
    youdao_asr.asr()
