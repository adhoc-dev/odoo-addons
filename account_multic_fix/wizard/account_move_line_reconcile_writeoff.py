# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api, _


class account_move_line_reconcile_writeoff(models.TransientModel):

    _inherit = 'account.move.line.reconcile.writeoff'

    @api.model
    def _get_company_id(self):
        active_ids = self._context.get('active_ids', [])
        statements = self.env['account.move.line'].browse(active_ids)
        company_ids = statements.mapped('company_id').ids
        if len(set(company_ids)) > 1:
            raise Warning(_('All move lines must be from the same company!'))
        return self.env['res.company'].search(
            [('id', 'in', company_ids)], limit=1)

    company_id = fields.Many2one(
        'res.company',
        'Company',
        required=True,
        default=_get_company_id)

    @api.multi
    def trans_rec_reconcile(self):
        self.ensure_one()
        super(account_move_line_reconcile_writeoff, self.with_context(
            company_id=self.company_id.id)).trans_rec_reconcile()
