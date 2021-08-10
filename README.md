# FUCK NCoV ZJGSU

[浙江工商大学 云战疫 自动报送](https://github.com/Hukeqing/FUCK-NCO-ZJGSU)的GitHub Action实现

## 食用方法
### 第一步
Fork本仓库，而后在Settings-Secrets中添加以下secret
|变量名|含义|
| --- | --- |
|NAME |用户名（学号）|
|PASSWORD|密码|

### 第二步
到Action页面，启用workflow。然后随意修改`README.md`并提交一次commit，检查workflow运行情况

此项目默认会在每天十点左右上午执行，如需变更请修改`.github/workflows/main.yml`

如果一个项目超过60天不活跃，其workflow会被禁用。如需永动请参考https://github.com/zhzhzhy/Workflow-Keep-Alive

# 本代码使用 GPL 3.0 开源，请遵循 GPL 3.0 进行开发使用
# 仅供学习交流使用，如有意外，自行承担责任
