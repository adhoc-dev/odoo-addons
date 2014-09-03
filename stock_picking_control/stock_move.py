from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

class stock_move_consume(osv.osv_memory):
    
    _inherit = 'stock.partial.picking.line'

    def _check_quantity(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        if obj.move_id.product_qty < obj.quantity:
            print obj.move_id
            return False
        else:
            return True

    _constraints = [(_check_quantity, _('Quantity to send can not be greater than the remaining quantity for this move.'), ['quantity'])]
