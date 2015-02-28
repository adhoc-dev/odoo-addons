# -*- coding: utf-8 -*-
from openerp.osv import osv


class sale_sales_to_sale_order_wizard(osv.osv_memory):
    _name = 'sale.sales_to_sale_order_wizard'
    _description = 'Generate Sale Order from Sales Orders'

    def action_group(self, cr, uid, ids, context=None):
        ''' Hicimos este wizard y esta accion porque no sabiamos como crear la
        accion que llame directamente a la funcion, solo sabiamos desde un
        act_window'''

        active_ids = context.get('active_ids', False)
        if not active_ids:
            return False
        return self.pool['sale.order'].copy_and_group_sale_orders(
            cr, uid, active_ids, context=context)
