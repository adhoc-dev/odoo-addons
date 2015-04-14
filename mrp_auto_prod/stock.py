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

    @api.cr_uid_ids_context
    def do_prepare_partial(self, cr, uid, picking_ids, context=None):
        for move in self.browse(cr, uid, picking_ids).move_lines:
            mrp_obj = self.pool['mrp.production']
            if move.state in ('done', 'cancel'):
                continue
            product_qty = move.product_uom_qty
            orders_prod = mrp_obj.search(
                cr, uid, [('move_prod_id', '=', move.id)])
            production = False
            if not orders_prod == []:
                production = mrp_obj.browse(cr, uid, orders_prod)
            if production:
                if production.bom_id and production.bom_id.auto_produce_on_picking:
                    remaining_prod_qty = self._get_product_qty(
                        cr, uid,
                        production.id, context=context)
                    if remaining_prod_qty < product_qty:
                        product_qty = remaining_prod_qty
                    self.pool['mrp.production'].action_produce(
                        cr,
                        uid,
                        production.id,
                        product_qty,
                        'consume_produce',
                        context=context)
                    self.pool['mrp.production'].action_production_end(
                        cr,
                        uid,
                        [production.id],
                        context=context)
        res = super(stock_picking, self).do_prepare_partial(
            cr, uid, picking_ids)
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
