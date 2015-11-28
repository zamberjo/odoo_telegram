# -*- coding: utf-8 -*-
# (c) 2015 Jose Zambudio Bernabeu
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


import logging
_logger = logging.getLogger("[TELEGRAM_HANDLERS]")

import openerp.tools.config as config
from telebot import types
from openerp import SUPERUSER_ID, api, sql_db
from contextlib import closing

MESSAGE_MODELS = [
    ('res.partner', 'To partner'),
    ('res.users', 'To user'),
    ('res.employee', 'To employee'),
]


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

        @BOT.message_handler(commands=['ping'])
        def _handle_ping(message):
            _logger.info("_handle_ping: %r" % (message))
            BOT.reply_to(message, 'pong!')

        def _step_do_message(message):
            _logger.info("_step_do_message:")
            _logger.info(message)
            markup = types.ReplyKeyboardHide(selective=False)
            with api.Environment.manage():
                env = api.Environment(
                    self.get_cursor(), self.uid, self.context)
                with closing(env.cr):
                    try:
                        MailMessage = env['mail.message']
                        ResPartner = env['res.partner']
                        from_user = ResPartner.search([
                            ('telegram_id', '=', message.from_user.id)
                        ])
                        _logger.info('from_user = %r' % (from_user))
                        MailMessage.create({
                            'type': 'comment',
                            'author_id': from_user.id,
                            'notified_partner_ids': [
                                (6, False, from_user.notified_telegram.ids)],
                            'subtype_id': 1,
                            'body': message.text,
                        })
                    except Exception, e:
                        _logger.exception("Step 2: %s" % str(e))
                        BOT.reply_to(
                            message,
                            "Step 3: ERROR - Vuelva a intentarlo en unos "
                            "minutos.",
                            reply_markup=markup)
                    else:
                        BOT.reply_to(
                            message, 'Mensaje enviado!', reply_markup=markup)
                    finally:
                        env.cr.commit()

        def _step_ask_message(message):
            _logger.info("_step_ask_message: %r" % (message))
            markup = types.ReplyKeyboardHide(selective=False)
            with api.Environment.manage():
                env = api.Environment(
                    self.get_cursor(), self.uid, self.context)
                with closing(env.cr):
                    try:
                        ResPartner = env['res.partner']
                        # Save message to...
                        from_partner = ResPartner.search(
                            [('telegram_id', '=', message.from_user.id)])
                        notified_partner = ResPartner.search([
                            ('name', '=', message.text),
                        ])
                        from_partner.notified_telegram = [
                            (6, False, notified_partner.ids)
                        ]
                    except Exception, e:
                        _logger.error(e)
                        BOT.reply_to(
                            message,
                            "Step 3: ERROR - Vuelva a intentarlo en unos "
                            "minutos.",
                            reply_markup=markup)
                    finally:
                        env.cr.commit()
            msg = BOT.reply_to(
                message, 'Escribe el mensaje a enviar', reply_markup=markup)
            BOT.register_next_step_handler(msg, _step_do_message)

        def _step_select_model(message):
            _logger.info("_step_select_model: %r" % (message))
            markup = types.ReplyKeyboardMarkup()
            _logger.info("db_name = %r" % (config['db_name']))
            with api.Environment.manage():
                env = api.Environment(
                    self.get_cursor(), self.uid, self.context)
                with closing(env.cr):
                    try:
                        for model in MESSAGE_MODELS:
                            if message.text == model[1]:
                                # pooler
                                Model = env[model[0]]
                                _logger.info("model = %r" % (model[0]))
                                # records ids
                                records = Model.search([
                                    ('telegram_id', '!=', False)
                                ])
                                _logger.info("records = %r" % (records))

                        for record in records:
                            markup.row("%s" % (record.name_get()[0][1]))
                        msg = BOT.reply_to(
                            message,
                            "Step 2: Elija un registro",
                            reply_markup=markup)
                        BOT.register_next_step_handler(msg, _step_ask_message)
                    except Exception, e:
                        _logger.exception("Step 2: %s" % str(e))
                        markup = types.ReplyKeyboardHide(selective=False)
                        BOT.reply_to(
                            message,
                            "Step 2: ERROR - Vuelva a intentarlo en unos "
                            "minutos.",
                            reply_markup=markup)

        @BOT.message_handler(commands=['send_message'])
        def _handle_send_message(message):
            _logger.info("_handle_send_message: %r" % (message))
            markup = types.ReplyKeyboardMarkup()
            for model in MESSAGE_MODELS:
                markup.row("%s" % (model[1]))
            msg = BOT.reply_to(
                message, 'Step 1: Elija un perfil', reply_markup=markup)
            BOT.register_next_step_handler(msg, _step_select_model)

        _logger.info("message_handlers = %r" % (self.bot.message_handlers))
