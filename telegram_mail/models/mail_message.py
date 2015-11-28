# -*- coding: utf-8 -*-
# (c) 2015 Jose Zambudio Bernabeu - Zamberjo
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


import logging
_logger = logging.getLogger('[TELEGRAM_MAIL]')

from openerp import api, models, SUPERUSER_ID
from openerp.service.telegram import BOT


class MailMessage(models.Model):
    _inherit = 'mail.message'

    def _get_default_from(self, cr, uid, context=None):
        try:
            super(MailMessage, self)._get_default_from(
                cr, uid, context=context)
        except Exception, e:
            this = self.pool.get('res.users').browse(
                cr, SUPERUSER_ID, uid, context=context)
            if this.telegram_id and this.alias_domain:
                return 'email@default.com'
            raise e

    def _notify(self, cr, uid, newid, context=None, force_send=False,
                user_signature=True):
        _logger.info("MailMessage:: _notify(%r, %r, %r, %r, %r, %r, %r)" % (
            self, cr, uid, newid, context, force_send, user_signature))
        self.pool.get('mail.notification')._notify_telegram(cr, uid, [], newid)
        return super(MailMessage, self)._notify(
            cr, uid, newid,
            context=context,
            force_send=force_send,
            user_signature=user_signature)


class MailNotification(models.Model):
    _inherit = 'mail.notification'

    @api.multi
    def _notify_telegram(self, message_id):
        message = self.env['mail.message'].browse(message_id)
        _logger.info("MailNotification:: _notify_telegram(%r, %r)" % (
            self, message_id))
        if message.subject or message.body:
            _logger.info(
                "MailNotification:: message.subject=%r" % (message.subject))
            _logger.info("MailNotification:: message.body=%r" % (message.body))
            message_text = "\n".join([
                "El usuario %s te ha enviado el siguiente mensaje:" % (
                    message.author_id.name),
                message.subject or '',
                message.body or ''
            ])
            _logger.info("MailNotification:: message_text=%r" % (message_text))
            for partner in message.author_id.notified_telegram:
                _logger.info("MailNotification:: partner=%r" % (partner))
                if partner.telegram_id:
                    _logger.info(
                        "MailNotification:: Enviando a (%s) %s el siguiente "
                        "mensaje:\n%s" % (
                            partner.telegram_id, partner.name, message_text))
                    BOT.send_message(partner.telegram_id, message_text)

    """
    @api.multi
    def _notify_email(self, message_id, force_send=False, user_signature=True):
        _logger.info("_notify_email:: message_id=%r" % (message_id))
        _logger.info("_notify_email:: force_send=%r" % (force_send))
        _logger.info("_notify_email:: user_signature=%r" % (user_signature))
        # Overwrite method to add telegram notification
        self._notify_telegram(
            message_id, force_send=force_send, user_signature=user_signature)
        return super(MailNotification, self)._notify_email(
            message_id, force_send=force_send, user_signature=user_signature)
    """
