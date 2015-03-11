# -*- coding: utf-8 -*-
from openerp import models, api, fields


class account_voucher(models.Model):

    _inherit = "account.voucher"

    available_journal_ids = fields.Many2many(
        'account.journal',
        compute='_get_available_journals',
        string='Available Journals',
        )

    @api.one
    @api.depends('type')
    def _get_available_journals(self):
        self.available_journal_ids = self.env['account.journal']
        journal_ids = []
        if self.company_id:
            domain = [
                ('company_id', '=', self.company_id.id),
                ('type', 'in', ('cash', 'bank'))]
            if self._context.get('type', False) == 'payment':
                domain.append(('direction', 'in', [False, 'out']))
            elif self._context.get('type', False) == 'receipt':
                domain.append(('direction', 'in', [False, 'in']))
        journal_ids = self.env['account.journal'].search(domain)
        self.available_journal_ids = journal_ids

    @api.onchange('type')
    def on_change_company_new_api(self):
        self.journal_id = self.available_journal_ids and self.available_journal_ids[0].id or False
