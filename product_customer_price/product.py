# -*- coding: utf-8 -*-



import re
from openerp import netsvc
from openerp.osv import osv, fields
import openerp.addons.decimal_precision as dp

class product_customer_price(osv.osv):
    """"""
    
    _name = 'product.customer_price'
    _description = 'Product Customer Price'

    _columns = {
        'product_id': fields.many2one('product.product', string='Product', required=True, ondelete="cascade",),
        'partner_id': fields.many2one('res.partner', string='Partner', required=True, domain=[('customer','=',True)], context={'default_customer':True}),
        'price': fields.float('Price', digits_compute=dp.get_precision('Price'), help="Sale Price for this customer."),
    }

    _defaults = {
    }

    _constraints = [
    ]

class product(osv.osv):
    """"""
    
    _inherit = 'product.product'

    _columns = {
        'customer_price_ids': fields.one2many('product.customer_price', 'product_id', string='Customer Prices'),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
