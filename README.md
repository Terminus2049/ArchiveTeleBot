# ArchiveTeleBot

网页存档机器人 <http://t.me/Archive2049Bot>

<http://206.189.252.32:8088/>

附带自动检测保存的网页是否仍然有效。

**注意**：会将提交的网址保存在 archive.csv 文件中，并自动检测网页是否已经404。检测结果保存在 archive2.csv 中。

## 自行部署方法

1. 向 <http://t.me/BotFather> 申请 Token，填入 `ArchiveTeleBot.py` 中的 `bot = telebot.TeleBot("TOKEN")`。

2. 服务器部署

**注意**：使用自建存档需要安装 <https://github.com/Y2Z/monolith>

仅支持 python3。

```bash

pip install archivenow
pip install requests
pip install pyTelegramBotAPI bs4
```

使用

```python
python ArchiveTeleBot.py
```

自动检测网址：

  ```R
  R CMD BATCH check_archive.R
  ```
