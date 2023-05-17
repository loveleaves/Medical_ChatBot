# -*- coding:utf-8 -*-
import os


class FfmpegTool:
    """
    function: 利用ffmpeg处理音频
    resources:
        ffmpeg官网：https://www.ffmpeg.org/
        ffmpeg的github地址：https://github.com/FFmpeg/FFmpeg
    """

    def __init__(self):
        pass

    def convert_datatype(self, input_file_path: str, output_file_path: str, **kwargs) -> bool:
        """
        function: 转换音频文件格式
        """
        command_arr = ["ffmpeg"]
        command_arr.append("-i " + input_file_path.strip())

        if 'sample_rate' in kwargs:
            sample_rate = kwargs['sample_rate']
        else:
            sample_rate = 16000
        command_arr.append("-ar " + str(sample_rate))

        if 'nchannels' in kwargs:
            nchannels = kwargs['nchannels']
        else:
            nchannels = 1
        command_arr.append("-ac " + str(nchannels))

        command_arr.append(output_file_path.strip())

        conmmand_str = " ".join(command_arr)
        try:
            os.system(conmmand_str)
            return True
        except Exception as e:
            print(e)
            return False
