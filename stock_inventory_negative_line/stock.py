# -*- coding: utf-8 -*-
from openerp import models, osv, _
# from openerp.osv import fields, osv


class stock_picking(models.Model):
    _inherit = 'stock.inventory'

    def action_done(self, cr, uid, ids, context=None):
        """ Finish the inventory
        @return: True
        """
        for inv in self.browse(cr, uid, ids, context=context):
            # for inventory_line in inv.line_ids:
                # if inventory_line.product_qty < 0 and inventory_line.product_qty != inventory_line.theoretical_qty:
                    # raise osv.except_osv(_('Warning'), _('You cannot set a negative product quantity in an inventory line:\n\t%s - qty: %s' % (inventory_line.product_id.name, inventory_line.product_qty)))
            self.action_check(cr, uid, [inv.id], context=context)
            self.write(cr, uid, [inv.id], {'state': 'done'}, context=context)
            self.post_inventory(cr, uid, inv, context=context)
        return True
