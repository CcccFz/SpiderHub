# -*- coding: utf-8 -*-

from flask import Flask
from flask_pymongo import PyMongo

# 创建项目对象
app = Flask(__name__)

# 加载配置文件内容
app.config.from_object('show.setting')     # 模块下的setting文件名，不用加py后缀
app.config['MONGO_HOST'] = '127.0.0.1'
app.config['MONGO_PORT'] = 27017
app.config['MONGO_DBNAME'] = 'jobs'

# MongoDB
mongo = PyMongo(app, config_prefix='MONGO')

from show.controller import index