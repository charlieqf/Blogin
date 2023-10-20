"""
# coding:utf-8
@Time    : 2020/10/12
@Author  : charles feng
@File    : wsgi
"""
from blogin import create_app

app = create_app('production')
