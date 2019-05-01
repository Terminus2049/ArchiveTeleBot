# ArchiveTeleBot
A telegram bot to save url to [archive.is](https://archive.is/).

可以直接使用 <http://t.me/Archive2049Bot>，会忽略一切非 url 消息。

**注意**：会将提交的网址保存在 archive.csv 文件中，并自动检测网页是否已经404。检测结果保存在 archive2.csv 中。

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

自动检测网址：

  ```R
  R CMD BATCH check_archive.R
  ```
