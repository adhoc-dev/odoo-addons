# -*- coding: utf-8 -*-
from openerp import models, fields


class account_journal(models.Model):
    _inherit = "account.journal"

    allow_direct_payment = fields.Boolean(
        'Allow Direct Payment?',
        help='Can be used on direct payment on invoices?',
        )
