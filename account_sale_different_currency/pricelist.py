# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import fields, models


class product_pricelist(models.Model):

    _inherit = 'product.pricelist'

    invoice_in_different_currency_id = fields.Many2one(
        'res.currency',
        'Invoice in different Currency?',
        help='If you want the invoice in a different currency from the sale '
        'order, please select a currency'
        )
