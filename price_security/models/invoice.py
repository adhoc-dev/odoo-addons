# -*- coding: utf-8 -*-
from openerp import fields, models, api


class account_invoice_line(models.Model):
    _inherit = 'account.invoice.line'

    product_can_modify_prices = fields.Boolean(
        related='product_id.can_modify_prices',
        readonly=True,
        string='Product Can modify prices')

    @api.one
    @api.constrains(
        'discount', 'product_can_modify_prices')
    def check_discount(self):
        if self.user_has_groups('price_security.group_restrict_prices') and not self.product_can_modify_prices and self.invoice_id:
            self.env.user.check_discount(
                self.discount,
                self.invoice_id.partner_id.property_product_pricelist.id)
