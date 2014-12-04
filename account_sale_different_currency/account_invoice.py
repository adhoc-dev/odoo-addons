# -*- coding: utf-8 -*-
# from openerp.tools.translate import _
from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp


class account_invoice_line(osv.osv):

    _inherit = 'account.invoice.line'

    _columns = {
        'sale_currency_price_unit': fields.float(
            'Unit Price', required=True,
            digits_compute=dp.get_precision('Product Price')),
    }
