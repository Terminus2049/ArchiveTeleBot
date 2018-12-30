# ArchiveTeleBot
A telegram bot to save url to [archive.is](https://archive.is/).

可以直接使用 <http://t.me/Archive2049Bot>，会忽略一切非 url 消息。

## 自行部署方法

1. 向 <http://t.me/BotFather> 申请 Token，填入 `ArchiveTeleBot.py` 中的 `bot = telebot.TeleBot("TOKEN")`。

2. 服务器部署

只支持 python2。

```bash

pip install archivenow
pip install requests==2.5.3
```

使用

```python
python2 ArchiveTeleBot.py
```
