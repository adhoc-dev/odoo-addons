# -*- coding: utf-8 -*-
from openerp.osv import fields, osv


class product_template(osv.osv):

    _inherit = 'product.template'

    _columns = {
        'salesman_group_ids': fields.many2many(
            'sale.salesman.group', 'prod_template_salesgroup_rel',
            'template_id', 'section_id', string='Salesman Group', ),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
