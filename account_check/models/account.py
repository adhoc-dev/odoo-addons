# -*- coding: utf-8 -*-
from openerp import models, fields, api, _


class account_journal(models.Model):
    _inherit = 'account.journal'

    check_type = fields.Selection(
        [('issue', 'Issue'), ('third', 'Third')],
        'Check Type',
        help='Choose check type, if none check journal then keep it empty.')
    checkbook_ids = fields.One2many(
        'account.checkbook', 'journal_id', 'Checkbooks',)
    collection_account_id = fields.Many2one(
        'account.account', 'Collection Account', domain=[('type', 'in', ['other', 'liquidity'])], help='Deposit account for collection.'
        )
    warrant_account_id = fields.Many2one(
        'account.account', 'Warrant Account', domain=[('type', 'in', ['other', 'liquidity'])], help='Deposit account for warrant.'
        )

    @api.model
    def _get_payment_subtype(self):
        selection = super(account_journal, self)._get_payment_subtype()
        selection.append(('check', _('Check')))
        selection.append(('promissory', _('Promissory Note')))
        return selection
