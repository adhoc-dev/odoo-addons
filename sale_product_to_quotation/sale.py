# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, api


class sale_order(models.Model):
    _inherit = "sale.order"

    @api.multi
    def add_products(self, product_ids):
        self.ensure_one()
        for product in self.env['product.product'].browse(product_ids):
            line_data = self.env['sale.order.line'].product_id_change(
                self.pricelist_id.id,
                product.id,
                qty=1,
                uom=product.uom_id.id,
                partner_id=self.partner_id.id)
            val = {
                'product_uom_qty': 1,
                'order_id': self.id,
                'product_id': product.id or False,
                'product_uom': product.uom_id.id,
                'price_unit': line_data['value'].get('price_unit'),
                'tax_id': [(6, 0, line_data['value'].get('tax_id'))],
            }
            self.env['sale.order.line'].create(val)
