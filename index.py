# -*- coding: utf-8 -*-
import os
import json
import requests
from requests.structures import CaseInsensitiveDict
from datetime import datetime
import pytz

def main(*args):
    header = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Redmi K30 Pro Zoom Edition Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3211 MMWEBSDK/20220303 Mobile Safari/537.36 MMWEBID/9693 MicroMessenger/8.0.21.2120(0x28001557) Process/toolsmp WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64',
        'Content-Type': 'application/json',
    }
    
    ID = os.environ["NAME"]
    PWD = os.environ["PASSWORD"]
    
    users = [
        {
            'gh': str(ID),
            'psswd': str(PWD)
        }
    ]

    for user in users:
        s = requests.session()
        response = s.post('https://yzy.zjgsu.edu.cn/cloudbattleservice/service/login', data=json.dumps(user), headers=header)
        token = json.loads(response.text)['data']['token']
        headers = CaseInsensitiveDict()
        headers["token"] = token
        response = s.get('https://yzy.zjgsu.edu.cn/cloudbattleservice/service/getDailyReport', headers=headers)
        reportDate = json.loads(response.text)['data']['item']['reportDate']
        reportDate = datetime.strptime(reportDate, '%Y-%m-%d %H:%M:%S').strftime("%Y-%m-%d")
        nowDate = datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d")
        if (reportDate == nowDate):
            print((nowDate), '报送情况： *主动报送*')
        else:
            headers["Content-Type"] = "application/json"
            data = """{"currentResd":"浙江省杭州市钱塘区钱塘区下沙浙江工商大学金沙港生活园区","fromHbToZj":"C","fromWtToHz":"B","meetCase":"C",
            "travelCase":"D","medObsv":"B","belowCase":"D","hzQrCode":"A","specialDesc":"无","deviceId":"","fromDevice":"WeChat",
            "isNewEpid":"否","location":"浙江省杭州市钱塘区钱塘区下沙浙江工商大学金沙港生活园区","coordinate":"120.379852,30.312492"}""".encode('utf-8')
            response = s.post('https://yzy.zjgsu.edu.cn/cloudbattleservice/service/add', data=data, headers=headers)
            print((nowDate), '报送情况：' + (
                '成功打卡' if response.json()['code'] == 20000 else '打卡失败！！！！！！'
            ))

if __name__ == '__main__':
    main()