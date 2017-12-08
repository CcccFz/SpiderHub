# -*- coding: utf-8 -*-

from urllib import urlencode
import requests
import json

if __name__ == '__main__':
    ak = 'oypA2SIRdugGHPMRDbowoQoqTa8wi7Nw'
    address = urlencode({'address': '成都市锦江区红星路三段99号银石广场'})
    print address
    req = requests.get('http://api.map.baidu.com/geocoder/v2/?%s&output=json&ak=%s' % (address, ak))
    print req.text

    address = urlencode({'address': '成都市火车南站地铁口'})
    req = requests.get('http://api.map.baidu.com/geocoder/v2/?%s&output=json&ak=%s' % (address, ak))
    print req.text

    req = requests.get('http://api.map.baidu.com/location/ip?%s&ak=%s&coor=bd09ll' % (urlencode({'ip': '120.78.58.71'}), ak))
    print req.text
    for k, v in json.loads(req.text)['content']['address_detail'].items():
        print '%s: %s' % (k, v)


