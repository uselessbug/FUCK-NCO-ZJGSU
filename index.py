# -*- coding: utf-8 -*-
import json
import requests
from requests.structures import CaseInsensitiveDict
from datetime import datetime
import pytz
import hashlib
from Crypto.Cipher import AES
import os


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

    def cbc_encrypt(plaintext: str) -> str:
        """
        AES-CBC 加密
        key 必须是 16(AES-128)、24(AES-192) 或 32(AES-256) 字节的 AES 密钥；
        初始化向量 iv 为随机的 16 位字符串 (必须是16位)，
        解密需要用到这个相同的 iv，因此将它包含在密文的开头。
        """
        key = 'ED7925CF8acd26B0'
        block_size = len(key)
        padding = (block_size - len(plaintext) % block_size) or block_size  # 填充字节

        iv = '3670759D768a359f'
        mode = AES.new(key.encode(), AES.MODE_CBC, iv.encode())
        ciphertext = mode.encrypt((plaintext + padding * chr(padding)).encode())

        return ciphertext.hex()

    for user in users:
        s = requests.session()
        response = s.post('https://yzy.zjgsu.edu.cn/cloudbattleservice/service/cloudLogin', data=json.dumps(user),
                          headers=header)
        token = json.loads(response.text)['data']['token']
        headers = CaseInsensitiveDict()
        t = str(int(datetime.now().timestamp() * 1000))
        tp = t + '26B0'
        headers["zjgsuAuth"] = hashlib.md5(
            (user['gh'] + '*' + tp + '^25A622DCE625882D8085CC9F00BF8C12').encode('utf-8')).hexdigest()
        headers['zjgsuCheck'] = cbc_encrypt('882D' + tp)
        headers["token"] = token
        response = s.get('https://yzy.zjgsu.edu.cn/cloudbattleservice/service/getDailyReport', headers=headers)
        reportDate = json.loads(response.text)['data']['item']['reportDate']
        reportDate = datetime.strptime(reportDate, '%Y-%m-%d %H:%M:%S').strftime("%Y-%m-%d")
        nowDate = datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d")
        if reportDate == nowDate:
            print(nowDate, '报送情况： *主动报送*')
        else:
            headers["Content-Type"] = "application/json"
            # currentResd,location和coordinate按照需要修改成你的值
            data = """{"hzQrCode":"A","meetCase":"C","fromHbToZj":"C","isNewEpid":"否","deviceId":"","fromDevice":"WeChat",
            "location":"1919810","medObsv":"B","coordinate":"114,514",
            "currentResd":"114514","fromWtToHz":"B","travelCase":"D"}""".encode('utf-8')
            response = s.post('https://yzy.zjgsu.edu.cn/cloudbattleservice/service/add', data=data, headers=headers)
            print(nowDate, '报送情况：' + (
                '成功打卡' if response.json()['code'] == 20000 else '打卡失败！！！！！！'
            ))

if __name__ == '__main__':
    main()