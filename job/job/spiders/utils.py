# -*- coding: utf-8 -*-

import json
import requests


def convert(place):
    response = requests.get('http://api.map.baidu.com/geocoder/v2/', {'address': '%s' % place, 'city': '成都', 'ak': '8B6qF8mlCArn4bw2okOTNLGG7hMCtqRy', 'output': 'json'})
    data = json.loads(response.text)
    return data['result']['location']['lng'], data['result']['location']['lat']
