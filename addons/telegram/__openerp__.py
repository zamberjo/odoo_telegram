# -*- coding: utf-8 -*-
# (c) 2015 Jose Zambudio Bernabeu - Zamberjo
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


{
    'name': 'Telegram - Base',
    'version': '1.0',
    'category': 'Social Network',
    'sequence': 3,
    'summary': 'Telegram bot integration on odoo',
    'author': 'Jose Zambudio Bernabeu',
    'website': 'http://www.josezambudiobernabeu.com/',
    'depends': ['base'],
    'data': [
        'views/partner.xml',
        'views/users.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
}
