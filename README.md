# FUCK NCO ZJGSU

浙江工商大学 云战役 自动报送

## 需要
 1. 一台 Linux 系统的服务器
 2. git
 3. python3

## 部署使用
请先在服务器上进行如下操作

将代码复制至目标文件夹下

```shell script
cd /root/
git clone https://github.com/Hukeqing/FUCK-NCO-ZJGSU.git
cd FUCK-NCO-ZJGSU
pip install -r requirements.txt
chmod +x start.sh
```

**然后修改 userExample.json 文件，并将文件重命名为 user.json**

然后为服务器添加定时任务
```shell script
crontab -e
```

添加下面的内容
```shell script
5 0 * * * /root/nco/start.sh
```

然后保存即可

# 仅供学习交流使用，如有意外，自行承担责任
