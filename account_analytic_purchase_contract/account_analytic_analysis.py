# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta
import datetime
import logging
import time

from openerp.osv import osv, fields
import openerp.tools
from openerp.tools.translate import _

from openerp.addons.decimal_precision import decimal_precision as dp


class account_analytic_account(osv.osv):
    _inherit = "account.analytic.account"

    def _prepare_invoice_data(self, cr, uid, contract, context=None):
        context = context or {}

        journal_obj = self.pool.get('account.journal')
        if contract.type == 'purchase_contract':
            invoice = {}
            if not contract.partner_id:
                raise osv.except_osv(_('No Supplier Defined!'), _(
                    "You must first select a Supplier for Contract %s!") % contract.name)

            fpos = contract.partner_id.property_account_position or False
            journal_ids = journal_obj.search(cr, uid, [(
                'type', '=', 'purchase'), ('company_id', '=', contract.company_id.id or False)], limit=1)
            if not journal_ids:
                raise osv.except_osv(_('Error!'),
                                     _('Please define a pruchase journal for the company "%s".') % (contract.company_id.name or '', ))

            currency_id = False
            if contract.pricelist_id:
                currency_id = contract.pricelist_id.currency_id.id
            elif contract.partner_id.property_product_pricelist:
                currency_id = contract.partner_id.property_product_pricelist.currency_id.id
            elif contract.company_id:
                currency_id = contract.company_id.currency_id.id

            invoice = {
                'account_id': contract.partner_id.property_account_payable.id,
                'type': 'in_invoice',
                'reference': contract.name,
                'partner_id': contract.partner_id.id,
                'currency_id': currency_id,
                'journal_id': len(journal_ids) and journal_ids[0] or False,
                'date_invoice': contract.recurring_next_date,
                'origin': contract.code,
                'fiscal_position': fpos and fpos.id,
                'company_id': contract.company_id.id or False,
            }
            return invoice
        else:
            return super(account_analytic_account, self)._prepare_invoice_data(cr, uid, contract, context=context)

    def _prepare_invoice_lines(self, cr, uid, contract, fiscal_position_id, context=None):

        if not context:
            context = {}
        if contract.type == 'purchase_contract':
            fpos_obj = self.pool.get('account.fiscal.position')
            fiscal_position = None
            if fiscal_position_id:
                fiscal_position = fpos_obj.browse(
                    cr, uid,  fiscal_position_id, context=context)
            invoice_lines = []
            for line in contract.recurring_invoice_line_ids:

                res = line.product_id
                account_id = res.property_account_income.id
                if not account_id:
                    account_id = res.categ_id.property_account_income_categ.id
                account_id = fpos_obj.map_account(
                    cr, uid, fiscal_position, account_id)

                taxes = res.supplier_taxes_id or False
                if taxes:
                    tax_ids = [x.id for x in taxes]
                    tax_ids = self.pool['account.tax'].search(
                        cr, uid,
                        [('id', 'in', tax_ids), ('company_id', '=', contract.company_id.id)],
                        context=context)
                    taxes = self.pool['account.tax'].browse(cr, uid, tax_ids, context=context)
                tax_id = fpos_obj.map_tax(cr, uid, fiscal_position, taxes)

                invoice_lines.append((0, 0, {
                    'name': line.name,
                    'account_id': account_id,
                    'account_analytic_id': contract.id,
                    'price_unit': line.price_unit or 0.0,
                    'quantity': line.quantity,
                    'uos_id': line.uom_id.id or False,
                    'product_id': line.product_id.id or False,
                    'invoice_line_tax_id': [(6, 0, tax_id)],
                }))
            return invoice_lines
        else:
            return super(account_analytic_account, self)._prepare_invoice_lines(cr, uid, contract, fiscal_position_id, context=None)

    def _cron_recurring_create_invoice_purchase(self, cr, uid, context=None):
        current_date =  time.strftime('%Y-%m-%d')
        contract_ids = self.search(cr, uid, [('recurring_next_date', '<=', current_date), (
            'state', '=', 'open'), ('recurring_invoices', '=', True), ('type', '=', 'purchase_contract')])
        return self._recurring_create_invoice(cr, uid, contract_ids, context=context)
