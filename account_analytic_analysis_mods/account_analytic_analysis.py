# -*- coding: utf-8 -*-
from openerp import models


class account_analytic_account(models.Model):
    _inherit = "account.analytic.account"

    def _recurring_create_invoice(
            self, cr, uid, ids, automatic=False, context=None):
        invoice_ids = super(
            account_analytic_account, self)._recurring_create_invoice(
            cr, uid, ids, automatic=automatic, context=context)
        self.pool['account.invoice'].button_compute(
            cr, uid, invoice_ids, context=context)

    def _prepare_invoice_data(self, cr, uid, contract, context=None):
        invoice = super(account_analytic_account, self)._prepare_invoice_data(
            cr, uid, contract, context=context)
        if contract.type == 'contract':
            invoice['reference'] = contract.name
        return invoice

    def _prepare_invoice_lines(
            self, cr, uid, contract, fiscal_position_id, context=None):
        invoice_lines = super(
            account_analytic_account, self)._prepare_invoice_lines(
            cr, uid, contract, fiscal_position_id, context=None)

        if contract.type == 'contract':
            fiscal_position = None
            fpos_obj = self.pool['account.fiscal.position']
            if fiscal_position_id:
                fiscal_position = fpos_obj.browse(
                    cr, uid,  fiscal_position_id, context=context)

            for line in invoice_lines:
                tax_ids = line[2]['invoice_line_tax_id']
                if tax_ids:
                    tax_ids = tax_ids[0][2]
                    tax_ids = self.pool['account.tax'].search(
                        cr, uid,
                        [('id', 'in', tax_ids),
                         ('company_id', '=', contract.company_id.id)])
                    taxes = self.pool['account.tax'].browse(
                        cr, uid, tax_ids, context=context)
                    tax_ids = fpos_obj.map_tax(cr, uid, fiscal_position, taxes)
                    line[2]['invoice_line_tax_id'] = [(6, 0, tax_ids)]

        return invoice_lines
