#! /usr/bin/python3
# -*- coding: utf-8 -*- 
# @File     :setup.py
# @Time     :2021/2/1
# @Author   :jiawei.li
# @Software :PyCharm
# @Desc     :None
import setuptools


setuptools.setup(
    name='TEST_ETAE',
    version='0.0.2',
    auther='jiawei.li',
    auther_email='jiawei.li@shopee.com',
    description='A temp upload for ETA prediction',
    long_description_content_type="text/markdown",
    url='',
    packages=setuptools.find_packages(),
    classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
      ],
    python_reqires='>=3.6'
)
