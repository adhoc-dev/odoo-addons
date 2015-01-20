# -*- coding: utf-8 -*-
from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class account_invoice_tax_wizard(models.TransientModel):
    _name = 'account.invoice.tax.wizard'
    _description = 'Account Invoice Tax Wizard'

    @api.model
    def _get_invoice2(self):
        return self._context.get('active_id', False)

    tax_id = fields.Many2one('account.tax', 'Tax', required=True,)
    name = fields.Char(string='Tax Description', required=True)
    base = fields.Float(
        string='Base', digits=dp.get_precision('Account'), required=True)
    amount = fields.Float(
        string='Amount', digits=dp.get_precision('Account'), required=True)
    invoice_id = fields.Many2one(
        'account.invoice',
        'Invoice',
        default=_get_invoice2,
        # required=True
        )
    invoice_type = fields.Selection(
        related='invoice_id.type', string='Invoice Type')
    invoice_company_id = fields.Many2one(
        'res.company', string='Company',
        related='invoice_id.company_id')

    @api.onchange('tax_id')
    def onchange_tax(self):
        self.name = self.tax_id and ('%s - %s') % (
            self.tax_id.description, self.tax_id.name) or False

    @api.multi
    def confirm(self):
        active_id = self._context.get('active_id', False)
        if not active_id:
            return False
        invoice = self.env['account.invoice'].browse(active_id)
        val = {
            'invoice_id': active_id,
            'name': self.name,
            'manual': True,
            'base': self.base,
            'amount': self.amount,
        }
        if invoice.type in ('out_invoice', 'in_invoice'):
            val['base_code_id'] = self.tax_id.base_code_id.id
            val['tax_code_id'] = self.tax_id.tax_code_id.id
            val['base_amount'] = self.base * self.tax_id.base_sign
            val['tax_amount'] = self.amount * self.tax_id.tax_sign
            val['account_id'] = self.tax_id.account_collected_id.id
            val['account_analytic_id'] = self.tax_id.account_analytic_collected_id.id
        else:
            val['base_code_id'] = self.tax_id.ref_base_code_id.id
            val['tax_code_id'] = self.tax_id.ref_tax_code_id.id
            val['base_amount'] = self.base * self.tax_id.ref_base_sign
            val['tax_amount'] = self.amount * self.tax_id.ref_tax_sign
            val['account_id'] = self.tax_id.account_paid_id.id
            val['account_analytic_id'] = self.tax_id.account_analytic_paid_id.id

        self.env['account.invoice.tax'].create(val)
