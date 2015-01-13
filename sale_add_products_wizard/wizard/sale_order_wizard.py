# -*- coding: utf-8 -*-
from openerp import models, fields, api


class sale_order_add_multiple(models.TransientModel):
    _name = 'sale.order.add_multiple'
    _description = 'Sale order add multiple'

    quantity = fields.Float('Quantity',
                            default='1.0')
    products_ids = fields.Many2many(
        'product.product',
        string='Products',
        domain=[('sale_ok', '=', True)],
    )

    @api.one
    def add_multiple(self):
        active_id = self._context['active_id']
        sale = self.env['sale.order'].browse(active_id)
        for product_id in self.products_ids:
            product = self.env['sale.order.line'].product_id_change(
                sale.pricelist_id.id,
                product_id.id,
                qty=self.quantity,
                uom=product_id.uom_id.id,
                partner_id=sale.partner_id.id)
            val = {
                'name': product['value'].get('name'),
                'product_uom_qty': self.quantity,
                'order_id': active_id,
                'product_id': product_id.id or False,
                'product_uom': product_id.uom_id.id,
                'price_unit': product['value'].get('price_unit'),

            }
            self.env['sale.order.line'].create(val)
