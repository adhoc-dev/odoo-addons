# -*- coding: utf-8 -*-
from openerp import models, fields


class account_journal(models.Model):
    _inherit = 'account.journal'

    check_type = fields.Selection(
        [('issue', 'Issue'), ('third', 'Third')],
        'Check Type',
        help='Choose check type, if none check journal then keep it empty.')
    validate_only_checks = fields.Boolean(
        'Validate only Checks',
        help='If marked, when validating a voucher, verifies that the total amounth of the voucher is the same as the checks used.')
    checkbook_ids = fields.One2many(
        'account.checkbook', 'journal_id', 'Checkbooks',)
