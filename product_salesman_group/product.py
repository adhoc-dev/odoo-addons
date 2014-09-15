# -*- coding: utf-8 -*-
from openerp.osv import fields, osv


class product_product(osv.osv):

    _inherit = 'product.product'

    _columns = {
        'salesman_group_ids': fields.many2many(
            'sale.salesman.group', 'productsalesgroup_rel',
            'product_id', 'section_id', string='Salesman Group', ),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
