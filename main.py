import json
import uuid
import re
import datetime

user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'

data = {
    'currentResd': '',
    'fromHbToZjDate': '',
    'fromHbToZj': 'C',
    'fromWtToHzDate': '',
    'fromWtToHz': 'B',
    'meetDate': '',
    'meetCase': 'C',
    'travelDate': '',
    'travelCase': 'D',
    'medObsvReason': '',
    'medObsv': 'B',
    'belowCaseDesc': '',
    'belowCase': 'D',
    'temperature': '',
    'notApplyReason': '',
    'hzQRCode': 'A',
    'specialDesc': ''}

with open('user.json', encoding='utf-8') as f:
    fileData = json.load(f)
try:
    import requests

    for user in fileData["user"]:
        try:
            ui = uuid.uuid1()
            data['uuid'] = str(ui)
            data['currentResd'] = user['home']
            header = {'User-Agent': user_agent}
            res = requests.post('https://nco.zjgsu.edu.cn/login', data=user, headers=header)
            cookieValue = ''
            for item in res.cookies:
                cookieValue += item.name + '=' + item.value + ';'
            cookieValue += ' _ncov_uuid=' + str(ui) + '; _ncov_username=' + user['name'] + '; _ncov_psswd=' + user['psswd']

            header = {'User-Agent': user_agent,
                      'Cookie': cookieValue}

            res = requests.post('https://nco.zjgsu.edu.cn/', data=data, headers=header)
            result = re.search('报送成功', str(res.content, encoding='utf-8')) is not None
            print(datetime.datetime.now().strftime('%Y-%m-%d'), '报送情况：', result)
            assert result
        except Exception:
            import smtplib
            from email.mime.text import MIMEText

            msg = MIMEText('本次打卡出错，请手动打卡', 'plain', 'utf-8')
            server = smtplib.SMTP('smtp.qq.com', 25)
            server.login(fileData['email'], fileData['pwd'])
            server.sendmail(fileData['email'] + '@qq.com', user['email'], msg.as_string())
            server.quit()
except Exception:
    import smtplib
    from email.mime.text import MIMEText

    msg = MIMEText('系统出错', 'plain', 'utf-8')
    server = smtplib.SMTP('smtp.qq.com', 25)
    server.login(fileData['email'], fileData['pwd'])
    server.sendmail(fileData['email'] + '@qq.com', fileData['admin'], msg.as_string())
    server.quit()
