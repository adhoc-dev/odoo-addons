# -*- coding: utf-8 -*-
from openerp import fields, models, api, _
from openerp import tools
from openerp.tools import float_compare, DEFAULT_SERVER_DATETIME_FORMAT
import openerp.addons.decimal_precision as dp


class stock_move(models.Model):

    _inherit = "mrp.bom"

    auto_produce_on_picking = fields.Boolean(
        'Auto Produce on Picking',
        help='When validating a picking, \
            if picking move has a related Manufacturing Order, \
            then auto produce on delivery')


class stock_picking(models.Model):

    _inherit = "stock.picking"

    def _get_product_qty(self, cr, uid, production_id, context=None):
        """ To obtain product quantity
        @param self: The object pointer.
        @param cr: A database cursor
        @param uid: ID of the user currently logged in
        @param product_id: product_id
        @param context: A standard dictionary
        @return: Quantity
        """
        if context is None:
            context = {}
        prod = self.pool['mrp.production'].browse(
            cr,
            uid,
            production_id,
            context=context)
        done = 0.0
        for move in prod.move_created_ids2:
            if move.product_id == prod.product_id:
                if not move.scrapped:
                    done += move.product_qty
        return (prod.product_qty - done) or prod.product_qty




# class stock_transfer_details(models.TransientModel):
#     _inherit = 'stock.transfer_details'


#     @api.one
#     def do_detailed_transfer(self):

#         mrp_obj = self.env['mrp.production']
#         for items in self.item_ids:
#             if move.state in ('done', 'cancel'):
#                 continue
#             product_qty = items.quantity
#             if picking_id.backorder_id:
#                 picking_id = picking_id.backorder_id
#             orders_prod = mrp_obj.search(
#                 [('move_prod_id.picking_id', '=', picking_id.id)])
#             production = False
#             if not orders_prod == []:
#                 production = mrp_obj.browse(orders_prod.id)
#             if production:
#                 if production.bom_id and production.bom_id.auto_produce_on_picking:
#                     remaining_prod_qty = picking_id._get_product_qty(
#                         production.id)
#                     if remaining_prod_qty <= product_qty:
#                         product_qty = remaining_prod_qty
#                         production.action_produce(
#                             production.id,
#                             product_qty,
#                             'consume_produce')
#                         production.action_production_end()
#                     else:
#                         production.action_produce(
#                             production.id,
#                             product_qty,
#                             'consume_produce')
#                         production.action_in_production()
#         res = super(stock_transfer_details, self).do_detailed_transfer()
#         return res

   
