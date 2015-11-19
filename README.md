# Telegram bot integration on odoo

## Requeriments

* Install python requeriments

`pip install -r requeriments.txt`

## Installation

* Edit openerp/service/__init__.py and add this code on line 10:

`import telegram`

* Copy installation/telegram folder inside openerp/service/

`openerp/service/telegram/__ini__.py`

## Uses

```
from openerp.service.telegram import BOT
BOT.send_message(telegramUserId, 'Hello World!')
```

## Configuration

*  Add this lines

```
[config]
...
# TELEGRAM_BOT_APIKEY -> View BotFather
telegram_apikey = ...

# True/False (default False) - Don't stop polling when receiving an error
telegram_none_stop = ...

# True/False (default False) - The interval between polling requests
# Note: Editing this parameter harms the bot's response time
telegram_interval = ...

# True/False (default True) - Blocks upon calling this function
telegram_block = ...
...
```

## TODO

* Module telegram
* Integration module telegram with mail.messages
* Rethink everything again... hahaha :D

