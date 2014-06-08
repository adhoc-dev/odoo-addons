# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import osv, fields
import netsvc

class sale_order(osv.osv):

    _name = 'sale.order'
    _inherit = 'sale.order'

    
    def _create_pickings_and_procurements(self, cr, uid, order, order_lines, picking_id=False, context=None):
            """Create the required procurements to supply sale order lines, also connecting
            the procurements to appropriate stock moves in order to bring the goods to the
            sale order's requested location.

            If ``picking_id`` is provided, the stock moves will be added to it, otherwise
            a standard outgoing picking will be created to wrap the stock moves, as returned
            by :meth:`~._prepare_order_picking`.

            Modules that wish to customize the procurements or partition the stock moves over
            multiple stock pickings may override this method and call ``super()`` with
            different subsets of ``order_lines`` and/or preset ``picking_id`` values.

            :param browse_record order: sale order to which the order lines belong
            :param list(browse_record) order_lines: sale order line records to procure
            :param int picking_id: optional ID of a stock picking to which the created stock moves
                                   will be added. A new picking will be created if ommitted.
            :return: True
            """
            move_obj = self.pool.get('stock.move')
            picking_obj = self.pool.get('stock.picking')
            procurement_obj = self.pool.get('procurement.order')
            proc_ids = []

            for line in order_lines:
                if line.state == 'done':
                    continue

                date_planned = self._get_date_planned(cr, uid, order, line, order.date_confirm, context=context)

                if line.product_id:
                    if line.product_id.product_tmpl_id.type in ('product', 'consu'):
                        if not picking_id:
                            picking_id = picking_obj.create(cr, uid, self._prepare_order_picking(cr, uid, order, context=context))
                        move_id = move_obj.create(cr, uid, self._prepare_order_line_move(cr, uid, order, line, picking_id, date_planned, context=context))
                    else:
                        # a service has no stock move
                        move_id = False

                    proc_id = procurement_obj.create(cr, uid, self._prepare_order_line_procurement(cr, uid, order, line, move_id, date_planned, context=context))
                    proc_ids.append(proc_id)
                    line.write({'procurement_id': proc_id})
                    self.ship_recreate(cr, uid, order, line, move_id, proc_id)

            wf_service = netsvc.LocalService("workflow")
            if picking_id:
                wf_service.trg_validate(uid, 'stock.picking', picking_id, 'button_confirm', cr)

            for proc_id in proc_ids:
                wf_service.trg_validate(uid, 'procurement.order', proc_id, 'button_confirm', cr)

            val = {}
            if order.state == 'shipping_except':
                val['state'] = 'progress'
                val['shipped'] = False

                if (order.order_policy == 'manual'):
                    for line in order.order_line:
                        if (not line.invoiced) and (line.state not in ('cancel', 'draft')):
                            val['state'] = 'manual'
                            break
            order.write(val)
            return True


    def _prepare_order_picking(self, cr, uid, order, context=None):
        pick_name = self.pool.get('ir.sequence').get(cr, uid, 'stock.picking.out')
        print order.date_confirm
        return {
            'name': pick_name,
            'origin': order.name,
            'date': self.date_to_datetime(cr, uid, order.date_confirm, context),
            'type': 'out',
            'state': 'auto',
            'move_type': order.picking_policy,
            'sale_id': order.id,
            'partner_id': order.partner_shipping_id.id,
            'note': order.note,
            'invoice_state': (order.order_policy=='picking' and '2binvoiced') or 'none',
            'company_id': order.company_id.id,
        }


sale_order() 