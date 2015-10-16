# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api, _
from openerp.exceptions import Warning


class product_template(models.Model):
    _inherit = "product.template"

    sale_price_currency_id_copy = fields.Many2one(
        related='sale_price_currency_id',
        readonly=True,
        )

    @api.onchange(
        'list_price_type',
        'list_price_type_currency_id'
        )
    def change_list_price_type(self):
        # if we use type by_margin, then currency is the same as list_price
        # by_margin currency, we want to show it
        if self.list_price_type == 'by_margin':
            self.sale_price_currency_id = self.list_price_type_currency_id

    @api.constrains('sale_price_currency_id', 'list_price_type_currency_id')
    def check_currencies(self):
        if (
                self.list_price_type == 'by_margin' and
                self.sale_price_currency_id !=
                self.list_price_type_currency_id
                ):
            raise Warning(_(
                'If Saly Price Type is By Margin, Sale Price Currency must be '
                'the same as List Price Type Currency'))
