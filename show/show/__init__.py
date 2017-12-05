# -*- coding: utf-8 -*-

from flask import Flask
from flask_pymongo import PyMongo

# 创建项目对象
app = Flask(__name__)

# 加载配置文件内容
app.config.from_object('show.setting')

# MongoDB
app.config['MONGO_HOST'] = '127.0.0.1'
app.config['MONGO_PORT'] = 27017
app.config['MONGO_DBNAME'] = 'jobs'
mongo = PyMongo(app, config_prefix='MONGO')

# 自定义过滤器
app.jinja_env.filters['str2line'] = lambda s, x: '<br>'.join(s.split(x))

from show.controller import index
