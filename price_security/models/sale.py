# -*- coding: utf-8 -*-
from openerp import fields, models, api


class sale_order(models.Model):
    _inherit = 'sale.order'

    @api.one
    # Dummy depend so that it is updated on view load
    @api.depends('partner_id')
    def _get_user_restrict_prices(self):
        self.user_restrict_prices = self.env['res.users'].has_group(
            'price_security.group_restrict_prices')

    user_restrict_prices = fields.Boolean(
        compute='_get_user_restrict_prices',
        string='User Restrict Prices')


class sale_order_line(models.Model):
    _inherit = 'sale.order.line'

    @api.one
    # Dummy depend so that it is updated on view load
    @api.depends('product_id')
    def _get_user_restrict_prices(self):
        self.user_restrict_prices = self.env['res.users'].has_group(
            'price_security.group_restrict_prices')

    user_restrict_prices = fields.Boolean(
        compute='_get_user_restrict_prices',
        string='User Restrict Prices')
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
        'discount', 'user_restrict_prices', 'product_can_modify_prices')
    def check_discount(self):
        if self.user_restrict_prices and not self.product_can_modify_prices:
            self.env.user.check_discount(
                self.discount,
                self.order_id.pricelist_id.id)
