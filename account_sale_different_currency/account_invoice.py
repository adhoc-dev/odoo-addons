# -*- coding: utf-8 -*-
# from openerp.tools.translate import _
from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp


class account_invoice(osv.osv):

    _inherit = 'account.invoice'

    def _get_sale_currency_amount_total(
            self, cr, uid, ids, name, arg, context=None):
        res = {}
        for inv in self.browse(cr, uid, ids, context=context):
            res[inv.id] = inv.invoice_currency_rate and inv.amount_total / inv.invoice_currency_rate or False
        return res

    _columns = {
        'invoice_currency_rate': fields.float(
            'Invoice Currency Rate',
        ),
        'sale_currency_amount_total': fields.function(
            _get_sale_currency_amount_total, string='SO Currency Total',
            type='float', digits_compute=dp.get_precision('Account'),
        ),
        'sale_currency_id': fields.many2one(
            'res.currency', 'Sale Currency',
        ),
    }


class account_invoice_line(osv.osv):

    _inherit = 'account.invoice.line'

    _columns = {
        'sale_currency_price_unit': fields.float(
            'Unit Price in SO Currency', required=True,
            digits_compute=dp.get_precision('Product Price')),
    }
