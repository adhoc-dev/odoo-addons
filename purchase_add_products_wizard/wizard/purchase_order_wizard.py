# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api


class purchase_order_add_multiple(models.TransientModel):
    _name = 'purchase.order.add_multiple'
    _description = 'Purchase order add multiple'

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
        purchase = self.env['purchase.order'].browse(active_id)
        for product_id in self.products_ids:
            product = self.env['purchase.order.line'].product_id_change(
                purchase.pricelist_id.id,
                product_id.id,
                qty=self.quantity,
                uom_id=product_id.uom_po_id.id,
                partner_id=purchase.partner_id.id)
            val = {
                'name':  product['value'].get('name'),
                'product_uom_qty': self.quantity,
                'order_id': active_id,
                'product_id': product_id.id or False,
                'product_uom': product_id.uom_po_id.id,
                'date_planned': product['value'].get('date_planned'),
                'price_unit': product['value'].get('price_unit'),
                'taxes_id': [(6, 0, product['value'].get('taxes_id'))],
            }
            self.env['purchase.order.line'].create(val)
