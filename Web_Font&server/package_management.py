# -*- coding: utf-8 -*-
import os


# export the requirements
def export_package():
    # os.system("pipreqs ./ --encoding='utf-8' --force")
    os.system("pip freeze > requirements.txt")


# install the requirements
def import_package():
    os.system("pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple")


if __name__ == '__main__':
    export_package()
    # import_package()
