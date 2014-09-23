# -*- coding: utf-8 -*-
from openerp.osv import fields, osv


class stock_print_remit(osv.osv_memory):
    _name = 'stock.print_remit'
    _description = "Print Remit"

    _columns = {
        'remit_number': fields.char('Remit Number'),
    }

    def default_get(self, cr, uid, fields, context=None):
        res = super(stock_print_remit, self).default_get(
            cr, uid, fields, context=context)

        if 'active_id' not in context:
            return res

        picking_obj = self.pool.get('stock.picking')
        picking_id = context['active_id']
        picking = picking_obj.browse(cr, uid, picking_id, context=context)
        if isinstance(picking, list):
            picking = picking[0]

        print 'picking', picking
        if not picking.remit_number:
            picking_obj.set_remit_number(
                cr, uid, picking_id, context=context)
            picking = picking_obj.browse(cr, uid, picking_id, context=context)

        res['remit_number'] = picking.remit_number
        return res

    def recompute_sequence_number(self, cr, uid, ids, context=None):
        if 'active_id' not in context:
            return False

        picking_obj = self.pool.get('stock.picking')
        picking_id = context['active_id']
        picking = picking_obj.browse(cr, uid, picking_id, context=context)
        if isinstance(picking, list):
            picking = picking[0]

        picking_obj.set_remit_number(
            cr, uid, picking_id, context=context)
        picking = picking_obj.browse(cr, uid, picking_id, context=context)

        vals = {'remit_number': picking.remit_number}
        return {'value': vals}

    def print_stock_picking(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        picking_obj = self.pool['stock.picking']

        if 'active_id' not in context:
            return False
        picking_id = context['active_id']
        context['from_wizard'] = True

        return picking_obj.do_print_picking(
            cr, uid, picking_id, context=context)
