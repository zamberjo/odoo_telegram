# <p align="center">Odoo_Telegram
##<p align="center">Telegram bot integration on odoo

### Requeriments

* Install python requeriments

`pip install -r requeriments.txt`

This project uses the project [PyTelegramBotApi](https://github.com/eternnoir/pyTelegramBotAPI)

### Installation

* Edit openerp/service/__init__.py and add this code on line 10:

`import telegram`

* Copy installation/telegram folder inside openerp/service/

`openerp/service/telegram/__ini__.py`

### Usage

* Send message
```
from openerp.service.telegram import BOT
BOT.send_message(telegramUserId, 'Hello World!')
```

* For handle methods:
 * Adds "telegram" package on your addon, and "handlers" module python in it.
 * On handlers.py file, adds this code:
 * Example on `addons/telegram_mail
 ```
    from openerp import SUPERUSER_ID, api, sql_db
    ...

    class TelegramBotHandlers(object):
        def __init__(self, bot):
            self.bot = bot
            self.uid = SUPERUSER_ID
            self.context = {}

        def get_cursor(self):
            return sql_db.db_connect(config['db_name']).cursor()

        def handle(self):
            _logger.info('TelegramBotHandlers:handle -> %r' % (self.bot))
            BOT = self.bot
            ... adds BOT handlers here ...

            ... for example ...
            @BOT.message_handler(commands=['ping'])
            def handle_ping(message):
                BOT.reply_to(message, 'pong!')

            ... for odoo Environment ...
            @BOT.message_handler(commands=['ping'])
            def handle_ping(message):
                with api.Environment.manage():
                env = api.Environment(
                    self.get_cursor(), self.uid, self.context)
                with closing(env.cr):
                    try:
                        ResUsers = env['res.users']
                        ...
                        ResUSers.create({...})
                    except Exception, e:
                        ...
                    else:
                        env.cr.commit()
 ```

### Configuration

*  Add this lines

```
[config]
...
# TELEGRAM_BOT_APIKEY -> View BotFather
telegram_apikey = ...

# True/False (default False) - Do not stop polling when an ApiException occurs.
telegram_none_stop = ...

# True/False (default False) - The interval between polling requests
# Note: Editing this parameter harms the bot's response time
telegram_interval = ...

# True/False (default True) - Timeout in seconds for long polling.
telegram_timeout = ...
...
```


### TODO

* Security layer on telegram bot
* Module telegram
* Integration module telegram with mail.messages
* Notification state odoo server (down, up)
* Rethink everything again... hahaha :D
