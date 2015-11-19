# -*- coding: utf-8 -*-
# (c) 2015 Jose Zambudio Bernabeu - Zamberjo
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


import logging
_logger = logging.getLogger(__name__)

import telebot
import datetime
import threading
import openerp.tools.config as config
from openerp.service.server import ThreadedServer

BOT = None

start_bak = ThreadedServer.start

def telegram_thread(bot, telegram_none_stop, telegram_interval, telegram_block):
    _logger.info('ThreadedServer:: telegram-bot polling...')
    _logger.info('ThreadedServer:: bot = %r' % (bot))
    _logger.info('ThreadedServer:: telegram_none_stop = %r' % (telegram_none_stop))
    _logger.info('ThreadedServer:: telegram_interval = %r' % (telegram_interval))
    _logger.info('ThreadedServer:: telegram_block = %r' % (telegram_block))

    bot.polling(
        none_stop=telegram_none_stop, interval=telegram_interval, block=telegram_block)

def telegram_spawn():
    global BOT
    datetime.datetime.strptime('2012-01-01', '%Y-%m-%d')

    telegram_apikey = config.get('telegram_apikey')
    telegram_none_stop = config.get('telegram_none_stop', False)
    telegram_interval = config.get('telegram_interval', 0)
    telegram_block = config.get('telegram_block', True)
    if telegram_apikey:
        BOT = telebot.TeleBot(telegram_apikey)
        def target():
            telegram_thread(BOT, telegram_none_stop, telegram_interval, telegram_block)
        t = threading.Thread(target=target, name="openerp.service.telegrambot")
        t.setDaemon(True)
        t.start()
        _logger.info('ThreadedServer:: telegram-bot started!')
    else:
        _logger.warning("Telegram server not started! Please specify an bot api key!")

def new_start(self, stop=False):
    telegram_apikey = config['telegram_apikey']
    if telegram_apikey and not stop:
        telegram_spawn()
    start_bak(self, stop=stop)

ThreadedServer.start = new_start
