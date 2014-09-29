# -*- coding: utf-8 -*-


from openerp import netsvc
from openerp.osv import fields, orm

class res_company(orm.Model):

    _inherit = "res.company"
    _columns = {
        'sale_order_validity_days': fields.integer('Sale Order Vailidty Period', help='Set days of validity for Sales Order, if null, no validity date will be filled'),
    }


