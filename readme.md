# Ayaka Bot
基于OneBot V11协议的python异步QQ机器人

<img src="https://img.shields.io/badge/python-3.8%2B-blue">

# 安装
```bash
# 通过poetry纯净安装，如果没有请先安装poetry
pip install poetry

# install
poetry install
# 不同系统上一些包的依赖也可能不一样，因此如果运行时提示某些包缺失，自己装上就好（乐）

# start
poetry run python app.py
```
# go-cqhttp配置
分为两种情况

## 不修改ayaka bot
- 使用ws反向连接
- port `19900`
- ws地址 `ws://127.0.0.1:19900/ayakabot`

## 修改ayaka bot
当然，你也可以自己决定go-cqhttp的port、ws地址等，相应的，ayakabot需要修改：

`app.py:ayaka.run()` 修改run的port参数

`ayaka/driver.py:@app.websocket("/ayakabot")` 修改websocket的地址
