# -*- coding: utf-8 -*-
import datetime
import json
import re

import requests
from requests.structures import CaseInsensitiveDict

header = {
    'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;zfsoft',
}

data = """
{
    "place": "浙江省,杭州市,钱塘区,学正街18号",
    "coordinate": "120.388529,30.308752"
}
""".encode('utf-8')

with open('app-user.json', encoding='utf-8') as f:
    users = json.load(f)

for user in users:
    try:
        user["redirectUrl"] = "https://myapp.zjgsu.edu.cn/home/index"
        user["clientId"] = "qnFZATsB6D25EnZeII"
        user["mobileBT"] = "11111111-1111-1111-1111-111111111111"

        s = requests.session()
        res = s.post('https://uia.zjgsu.edu.cn/cas/mobile/getAccessToken', data=user, headers=header)
        access_token = res.json()['access_token']
        s.get('https://uia.zjgsu.edu.cn/cas/login?service=https://myapp.zjgsu.edu.cn/home/index&access_token=' + access_token + '&mobileBT=' + user['mobileBT'])

        res = s.get('https://ticket.zjgsu.edu.cn/stucheckservice/auth/login/stuCheck', headers=header)
        referer = res.history[-1].headers['location']
        token = re.search(R'\?token=(.+?)&', referer).group(1)
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Authorization"] = "Bearer " + token
        headers["token"] = token
        headers["Content-Type"] = "application/json"
        res = s.get('https://ticket.zjgsu.edu.cn/stucheckservice/service/getchecklist', headers=headers, data=data)
        if len(res.json()['data']['items']) > 0:
            print(datetime.datetime.now().strftime('%Y-%m-%d'), '报送情况： *主动报送*')
            continue
        res = s.post('https://ticket.zjgsu.edu.cn/stucheckservice/service/stuclockin', headers=headers, data=data)
        print(datetime.datetime.now().strftime('%Y-%m-%d'), '报送情况：' + (
            '成功打卡' if res.json()['code'] == 20000 else '打卡失败！！！！！！'
        ))
    except Exception as e:
        print(datetime.datetime.now().strftime('%Y-%m-%d'), '报送情况：打卡失败！！！！！！')
        continue
