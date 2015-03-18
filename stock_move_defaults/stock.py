# -*- coding: utf-8 -*-
from openerp import models, api


class stock_move(models.Model):

    _inherit = 'stock.move'

    @api.model
    def create(self, values):
        picking_type_id = self._context.get(
            'search_default_picking_type_id', False)
        if not values.get('location_dest_id'):
            values['location_dest_id'] = self.with_context(
                default_picking_type_id=picking_type_id)._default_location_destination()
        if not values.get('location_id'):
            values['location_id'] = self.with_context(
                default_picking_type_id=picking_type_id)._default_location_source()
        if values.get('product_id') and values.get('product_uom_qty') and any(f not in values for f in ['name', 'product_uom']):
            defaults = self.onchange_product_id(
                prod_id=values['product_id']
            )['value']
            values = dict(defaults, **values)
        return super(stock_move, self).create(values)
