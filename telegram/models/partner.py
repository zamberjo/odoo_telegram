# -*- coding: utf-8 -*-
# (c) 2015 Jose Zambudio Bernabeu - Zamberjo
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


import logging
_logger = logging.getLogger(__name__)

from openerp import api, fields, models
from openerp.tools.translate import _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    telegram_id = fields.Char('Telegram id')

    notify_telegram = fields.Selection(
        [
            ('none', 'Never'),
            ('always', 'All Messages'),
        ], 'Notifications by Telegram Bot', default='always',
        help="Policy to receive telegram messages for new messages pushed to your personal Inbox:\n"
                "- Never: no emails are sent\n"
                "- All Messages: for every notification you receive in your Inbox")
