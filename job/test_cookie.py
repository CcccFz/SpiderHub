# -*- coding: utf-8 -*-

import json
import requests

for i in range(100):
    # s = requests.session()
    # r = s.get('https://passport.lagou.com/login/login.json')
    r = requests.get('https://www.lagou.com/zhaopin/Python')
    print(r.request.headers)

