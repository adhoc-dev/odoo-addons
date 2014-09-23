# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
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
                raise osv.except_osv(_('No Supplier Defined!'),_("You must first select a Supplier for Contract %s!") % contract.name )

            fpos = contract.partner_id.property_account_position or False
            journal_ids = journal_obj.search(cr, uid, [('type', '=','purchase'),('company_id', '=', contract.company_id.id or False)], limit=1)
            if not journal_ids:
                raise osv.except_osv(_('Error!'),
                _('Please define a sale journal for the company "%s".') % (contract.company_id.name or '', ))


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

        if contract.type == 'purchase_contract':
            invoice = {}
            fpos_obj = self.pool.get('account.fiscal.position')
            fiscal_position = None
            if fiscal_position_id:
                fiscal_position = fpos_obj.browse(cr, uid,  fiscal_position_id, context=context)
            invoice_lines = []
            for line in contract.recurring_invoice_line_ids:

                res = line.product_id
                account_id = res.property_account_income.id
                if not account_id:
                    account_id = res.categ_id.property_account_income_categ.id
                account_id = fpos_obj.map_account(cr, uid, fiscal_position, account_id)

                taxes = res.taxes_id or False
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
        contract_ids = self.search(cr, uid, [('recurring_next_date','<=', current_date), ('state','=', 'open'), ('recurring_invoices','=', True), ('type', '=', 'purchase_contract')])
        invoice = self._recurring_create_invoice(cr, uid, contract_ids, context=context)
        return invoice


    


