# -*- coding: utf-8 -*-
from openerp.osv import osv
from openerp import fields


class inter_company_move_wizard(osv.osv_memory):

    _name = "inter_company_move_wizard"
    _description = "Inter Company Move Wizard"

    actual_company_id = fields.Many2one(
        'res.company',
        string='Actual Company',
        readonly=True)
    destiny_company_id = fields.Many2one(
        'res.company',
        string='Destiny Company',
        required=True)

    def action_confirm(self, cr, uid, ids, context=None):
        invoice_id = context.get('active_id', False)
        wizard = self.browse(cr, uid, ids, context=context)[0]
        if wizard and invoice_id:
            invoice = self.pool['account.invoice'].browse(
                cr, uid, invoice_id, context=context)
            return self.pool['account.invoice']._invoice_move(
                cr, uid, invoice, wizard.destiny_company_id, context=context)
