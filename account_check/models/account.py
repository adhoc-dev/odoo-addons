# -*- coding: utf-8 -*-
from openerp import models, fields


class account_journal(models.Model):
    _inherit = 'account.journal'

    check_type = fields.Selection(
        [('issue', 'Issue'), ('third', 'Third')],
        'Check Type',
        help='Choose check type, if none check journal then keep it empty.')
    checkbook_ids = fields.One2many(
        'account.checkbook', 'journal_id', 'Checkbooks',)
