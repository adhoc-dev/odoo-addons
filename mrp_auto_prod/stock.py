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

    def _get_product_qty(self, production_id, context=None):
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
        prod = self.env['mrp.production'].browse(
            production_id,
            context=context)
        done = 0.0
        for move in prod.move_created_ids2:
            if move.product_id == prod.product_id:
                if not move.scrapped:
                    done += move.product_qty
        return (prod.product_qty - done) or prod.product_qty

    @api.multi
    def do_partial(self, partial_datas, context=None):
        # uom_obj = self.pool.get('product.uom')
        # product_obj = self.pool.get('product.product')
        for move in self.move_lines:
            # new_picking = None
            # complete, too_many, too_few = [], [], []
            # partial_qty, product_uoms = {}, {}, {}, {}, {}
                # move_product_qty, prodlot_ids, product_avail,
            # partial_qty, product_uoms = {}, {}, {}, {}, {}
            if move.state in ('done', 'cancel'):
                continue
            partial_data = partial_datas.get('move%s' % (move.id), {})
            product_qty = partial_data.get(
                'product_qty',
                0.0)
            # product_uom = partial_data.get('product_uom',False)
            # move_product_qty[move.id] = product_qty
            # product_uoms[move.id] = product_uom
            # partial_qty[move.id] = uom_obj._compute_qty(cr, uid,
            #product_uoms[move.id], product_qty, move.product_uom.id)
            if move.procurements:
                production = move.procurements[0].production_id
                if production.bom_id and production.bom_id.auto_produce_on_picking:
                    remaining_prod_qty = self._get_product_qty(
                        production.id, context=context)
                    if remaining_prod_qty < product_qty:
                        product_qty = remaining_prod_qty
                    self.pool.get('mrp.production').action_produce(
                        production.id,
                        product_qty,
                        'consume_produce',
                        context=context)
        res = super(stock_picking, self).do_partial(
            partial_datas, context=context)
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
