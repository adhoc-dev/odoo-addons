# -*- coding: utf-8 -*-
from openerp import fields, models, api


class sale_order_line(models.Model):
    _inherit = 'sale.order.line'

    product_can_modify_prices = fields.Boolean(
        related='product_id.can_modify_prices',
        readonly=True,
        string='Product Can modify prices')
    # agregamos este campo porque si hacemos readonly el campo tax_id el impuesto puede ser sobre escritor por la funcion create de sale order line. de esta manera, oculamos tax para que escriba y ponemos esta copia readonly
    # tampoco nos anduvo porque no podiamos hacerlo visible segun el grupo
    # tax_id_copy = fields.Many2many(
    #     'account.tax',
    #     string='Taxes',
    #     related='tax_id',
    #     readonly=True
    #     )

    @api.one
    @api.constrains(
        'discount', 'product_can_modify_prices')
    def check_discount(self):
        if self.user_has_groups('price_security.group_restrict_prices') and not self.product_can_modify_prices:
            self.env.user.check_discount(
                self.discount,
                self.order_id.pricelist_id.id)
