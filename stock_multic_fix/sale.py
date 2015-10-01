# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################


from openerp import models, fields, api, _


class stock_invoice_onshipping(models.TransientModel):

    _inherit = 'stock.invoice.onshipping'

    @api.model
    def _get_company_id(self):
        active_ids = self._context.get('active_ids', [])
        stocks = self.env['stock.picking'].browse(active_ids)
        company_ids = [x.company_id.id for x in stocks]
        if len(set(company_ids)) > 1:
            raise Warning(_('All pickings must be from the same company!'))
        return self.env['res.company'].search(
            [('id', 'in', company_ids)], limit=1)

    company_id = fields.Many2one(
        'res.company',
        'Company',
        required=True,
        default=_get_company_id)

    @api.model
    def _get_journal(self):
        journal_obj = self.env['account.journal']
        journal_type = self._get_journal_type()
        company = self._get_company_id()
        journals = journal_obj.search(
            [('type', '=', journal_type),
             ('company_id', '=', company.id)])
        return journals and journals[0] or False

    _defaults = {
        'journal_id': _get_journal,
    }

    @api.multi
    def onchange_journal_id(self, journal_id):
        res = super(stock_invoice_onshipping, self).onchange_journal_id(
            journal_id)
        # remove domain that don't take in to account company and
        # dont do anything
        if res.get('domain'):
            res.pop('domain')
        return res
