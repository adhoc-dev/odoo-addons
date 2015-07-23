# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, api


class purchase_order_line(models.Model):
    _inherit = "purchase.order.line"

    @api.model
    def create(self, vals):

        if vals.get('order_id') and vals.get('product_id') and any(f not in vals for f in ['name', 'price_unit', 'date_planned', 'product_qty', 'product_uom']):
            order = self.env['purchase.order'].browse(
                vals['order_id'])
            defaults = self.onchange_product_id(
                order and order.pricelist_id.id or False,
                vals.get('product_id', False),
                vals.get('product_qty', False),
                vals.get('uom_id', False),
                order and order.partner_id.id or False,
            )['value']
            vals = dict(defaults, **vals)
        return super(purchase_order_line, self).create(vals)
