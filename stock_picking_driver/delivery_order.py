from openerp.osv import fields, osv
from openerp.tools.translate import _

class delivery_orders(osv.osv):
    
    _inherit = 'stock.picking.out'

    _columns = {
    'driver_id': fields.many2one('res.partner','Driver'),
    }

class stock_picking(osv.osv):
    
    _inherit = 'stock.picking'

    _columns = {
    'driver_id': fields.many2one('res.partner','Driver'),
    }

