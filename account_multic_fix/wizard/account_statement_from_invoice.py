# -*- coding: utf-8 -*-
from openerp import models, fields, api, _


class account_statement_from_invoice(models.TransientModel):

    _inherit = 'account.statement.from.invoice.lines'

    @api.model
    def _get_company_id(self):
        active_ids = self._context.get('active_ids', [])
        statements = self.env['account.bank.statement'].browse(active_ids)
        company_ids = [x.company_id.id for x in statements]
        if len(set(company_ids)) > 1:
            raise Warning(_('All statements must be from the same company!'))
        return self.env['res.company'].search(
            [('id', 'in', company_ids)], limit=1)

    company_id = fields.Many2one(
        'res.company',
        'Company',
        required=True,
        default=_get_company_id)
