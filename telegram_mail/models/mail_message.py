# -*- coding: utf-8 -*-
# (c) 2015 Jose Zambudio Bernabeu - Zamberjo
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


import logging
_logger = logging.getLogger(__name__)

from openerp import api, fields, models, SUPERUSER_ID
from openerp.tools.translate import _
from openerp.service.telegram import BOT


class MailMessage(models.Model):
    _inherit = 'mail.message'

    def _get_default_from(self, cr, uid, context=None):
        try:
            super(MailMessage, self)._get_default_from(cr, uid, context=context)
        except Exception, e:
            this = self.pool.get('res.users').browse(cr, SUPERUSER_ID, uid, context=context)
            if this.telegram_id and this.alias_domain:
                return 'email@default.com'
            raise e


class MailNotification(models.Model):
    _inherit = 'mail.notification'

    @api.multi
    def get_partners_to_telegram(self, message):
        notify_pids = []
        for notification in self:
            if notification.is_read:
                continue
            partner = notification.partner_id
            # Do not send to partners without telegram_id defined
            if not partner.telegram_id:
                continue
            # Do not send to partners having same telegram_id than the author (can cause loops or bounce effect due to messy database)
            if message.author_id and message.author_id.telegram_id == partner.telegram_id:
                continue
            # Partner does not want to receive any telegram messages or is opt-out
            if partner.notify_telegram == 'none':
                continue
            notify_pids.append(partner)
        return notify_pids

    @api.multi
    def _notify_telegram(self, message_id, force_send=False, user_signature=True):
        message = self.env['mail.message'].browse(message_id)
        if message.subject or message.body:
            message_text = "\n".join([
                "El usuario %s te ha enviado el siguiente mensaje:" % (message.author_id.name),
                message.subject or '',
                message.body or ''
            ])
            for partner in self.get_partners_to_telegram(message):
                if partner.telegram_id:
                    BOT.send_message(partner.telegram_id, message_text)


    @api.multi
    def _notify_email(self, message_id, force_send=False, user_signature=True):
        # Overwrite method to add telegram notification
        self._notify_telegram(message_id, force_send=force_send, user_signature=user_signature)
        return super(MailNotification, self)._notify_email(
            message_id, force_send=force_send, user_signature=user_signature)

