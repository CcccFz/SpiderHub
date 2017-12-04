# -*- coding: utf-8 -*-

from flask import Flask

# 创建项目对象
app = Flask(__name__)

# 加载配置文件内容
app.config.from_object('show.setting')     # 模块下的setting文件名，不用加py后缀

from show.controller import index