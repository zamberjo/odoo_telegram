# -*- coding: utf-8 -*-
# (c) 2015 Jose Zambudio Bernabeu - Zamberjo
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import os
import datetime
import threading
import logging
_logger = logging.getLogger('[TELEGRAM]')

import telebot
from telebot import types
from pydoc import locate

import openerp.tools.config as config
from openerp.modules import module
from openerp.service.server import ThreadedServer

BOT = None

start_bak = ThreadedServer.start

def telegram_thread(bot, telegram_none_stop, telegram_interval, telegram_timeout):
    _logger.debug('ThreadedServer:: telegram-bot polling...')
    _logger.debug('ThreadedServer:: bot = %r' % (bot))
    _logger.debug('ThreadedServer:: telegram_none_stop = %r' % (telegram_none_stop))
    _logger.debug('ThreadedServer:: telegram_interval = %r' % (telegram_interval))
    _logger.debug('ThreadedServer:: telegram_timeout = %r' % (telegram_timeout))

    def listener(messages):
        for m in messages:
            _logger.debug('listener = %r' % (m))

    bot.set_update_listener(listener)
    bot.polling(
        none_stop=bool(telegram_none_stop), interval=int(telegram_interval), timeout=int(telegram_timeout))

def telegram_spawn():
    global BOT
    datetime.datetime.strptime('2012-01-01', '%Y-%m-%d')

    telegram_apikey = config.get('telegram_apikey')
    telegram_none_stop = config.get('telegram_none_stop', False)
    telegram_interval = config.get('telegram_interval', 0)
    telegram_timeout = config.get('telegram_timeout', True)
    if telegram_apikey:
        _logger.debug("telebot.logger = %r" % (telebot.logger))
        telebot.logger.setLevel(logging.ERROR)
        _logger.debug("telebot.logger = %r" % (telebot.logger))
        BOT = telebot.TeleBot(telegram_apikey, threaded=False)

        # Handlers discovery
        try:
            _logger.debug("handlers discovery...")
            for m in module.get_modules():
                m_path = module.get_module_path(m)
                if os.path.isdir(os.path.join(m_path, 'telegram')):
                    _logger.debug("telegram handlers on path %r" % (os.path.join(m_path, 'telegram')))
                    TelegramBotHandlers = locate('openerp.addons.' + m + '.telegram.handlers.TelegramBotHandlers')
                    TelegramBotHandlers(BOT).handle()
                    _logger.debug('imported!')
        except Exception,e:
            _logger.error(e)
            raise e

        def target():
            telegram_thread(BOT, telegram_none_stop, telegram_interval, telegram_timeout)
        t = threading.Thread(target=target, name="openerp.service.telegrambot")
        t.setDaemon(True)
        t.start()
        _logger.debug('ThreadedServer:: telegram-bot started!')
    else:
        _logger.warning("Telegram server not started! Please specify an bot api key!")

def new_start(self, stop=False):
    telegram_apikey = config['telegram_apikey']
    if telegram_apikey and not stop:
        telegram_spawn()
    start_bak(self, stop=stop)

ThreadedServer.start = new_start
