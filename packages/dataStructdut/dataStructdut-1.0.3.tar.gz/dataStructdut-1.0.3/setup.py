'''
Description: 
Author: Tjg
Date: 2021-02-10 10:07:22
LastEditTime: 2021-02-10 19:25:03
LastEditors: Please set LastEditors
'''
# -*- coding:utf-8 -*-
try:
    from setuptools import setup, find_packages
except:
    from distutils.core import setup
from codecs import open
from os import path

#版本号
VERSION = '1.0.3'

#发布作者
AUTHOR = "tjg"

#邮箱
AUTHOR_EMAIL = "1205322591@qq.com"

#项目网址
URL = "https://github.com/ChinaVeryNb/dataStruct.git"

#项目名称
NAME = "dataStructdut"

#项目简介
DESCRIPTION = "This package provides all kinds of dataStructs."

#LONG_DESCRIPTION为项目详细介绍，这里取README.md作为介绍
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.txt'), encoding='ISO-8859-1') as f:
    LONG_DESCRIPTION = f.read()

#搜索关键词
KEYWORDS = ["dataStruct", "dut"]

#发布LICENSE
LICENSE = "MIT"

#包
PACKAGES = ["dataStruct"]

#具体的设置
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',

    ],
    #指定控制台命令
    entry_points={
        'console_scripts': [
        ],
    },
    keywords=KEYWORDS,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    packages=PACKAGES,
    install_requires=[],                        #依赖的第三方包:无
    include_package_data=True,
    zip_safe=True,
)
