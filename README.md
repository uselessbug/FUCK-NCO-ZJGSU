# FUCK NCO ZJGSU

浙江工商大学 云战役 自动报送


## 1月13日更新说明
学校新增了名为 `locationInfo` 的字段导致程序无法正常使用的问题现在已经修复。请执行 `rm -rf /root/FUCK-NCO-ZJGSU` 后重新执行[第一步](#第一步)

现在的程序会直接读取学校要求的参数个数和内容，并且根据上一次的填写信息自动填报和上一次基本上完全相同的信息，所以在 user 栏中不再需要家庭地址信息

如果需要更改家庭地址，请在自动填报的代码执行前主动打卡更新，本程序的打卡不会覆盖主动打卡的信息

## 需要
 1. 一台 Linux 系统的服务器
 2. git
 3. python3

## 部署使用
### 第一步
请先在服务器上进行如下操作

将代码复制至目标文件夹下

```shell script
cd /root/
git clone https://github.com/Hukeqing/FUCK-NCO-ZJGSU.git
cd FUCK-NCO-ZJGSU
pip install -r requirements.txt
chmod +x start.sh
```
**请注意，脚本使用的是 python3，如果下载包时使用了 python2 则会出现意料之外的情况**
**然后修改 userExample.json 文件，并将文件重命名为 user.json**

### 第二步
然后为服务器添加定时任务
```shell script
crontab -e
```

添加下面的内容
```shell script
5 0 * * * /root/FUCK-NCO-ZJGSU/start.sh
```
此行代码的表示会在凌晨0点5分时自动打卡，如果你需要调整自动打卡时间，请自行修改，例如如下代码为在早上 8 点 32 分自动打卡
```shell script
32 8 * * * /root/FUCK-NCO-ZJGSU/start.sh
```

然后保存即可

# 本代码使用 GPL 3.0 开源，请遵循 GPL 3.0 进行开发使用
# 仅供学习交流使用，如有意外，自行承担责任
