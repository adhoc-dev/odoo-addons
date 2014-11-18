# -*- coding: utf-8 -*-
from openerp import models, fields, api, _

class account_invoice_refund(models.TransientModel):

    _inherit = 'account.invoice.refund'

   
    @api.model
    def _get_invoice_id(self):
        return self._context.get('active_id', False)

    @api.one
    @api.depends('invoice_id')
    def _get_journal_type(self):
        if self.invoice_id.type == 'out_refund' or 'out_invoice':
            self.journal_type = 'sale_refund'
        elif self.invoice_id.type == 'in_refund' or 'in_invoice':
            self.journal_type = 'purchase_refund'

    invoice_id = fields.Many2one(
        'account.invoice',
        'Invoice',
        default=_get_invoice_id,
        store=True)

   
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        related='invoice_id.company_id'
        )

    journal_type = fields.Char(
        'Journal type',
        compute='_get_journal_type'
        )

    
    @api.model
    def _get_journal(self):
        company_id = self.company_id
        journal = self.env['account.journal'].search([('type', '=', self.journal_type), ('company_id','=',self.company_id.id)], limit=1)
        return journal and journal[0] or False

    _defaults = {
        'journal_id': _get_journal,
    }

    def compute_refund(self, cr, uid, ids, data_refund, context=None):
        res = super(account_invoice_refund, self).compute_refund(
            cr, uid, ids, data_refund, context=context)
        domain = res.get('domain', [])
        invoice_ids = context.get('active_ids', [])
        if not invoice_ids:
            return res
        sale_order_ids = self.pool['sale.order'].search(
            cr, uid, [('invoice_ids', 'in', invoice_ids)])
        invoice_obj = self.pool['account.invoice']
        refund_invoice_ids = invoice_obj.search(cr, uid, domain)
        origin = ', '.join([x.number for x in invoice_obj.browse(
            cr, uid, invoice_ids) if x.number])
        invoice_obj.write(cr, uid, refund_invoice_ids, {
            'origin': origin,
            })
        if not self.browse(cr, uid ,ids, context=context)[0].period:
            invoice_obj.write(cr, uid, refund_invoice_ids, {
            'period_id': invoice_obj.browse(cr, uid, invoice_ids)[0].period_id.id
            })
        for invoice_id in refund_invoice_ids:
            self.pool['sale.order'].write(
                cr, uid, sale_order_ids, {'invoice_ids': [(4, invoice_id)]})
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
