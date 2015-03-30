# -*- coding: utf-8 -*-
from openerp.osv import fields, osv


class res_company(osv.osv):

    _inherit = 'res.company'

    _columns = {
        'currency_adjust_product_id': fields.many2one(
            'product.product',
            'Currency Adjust Product',
            help='Adjut currency exchange product when invoicing in different currency than sale order currency',),
        'default_advance_product_id': fields.many2one(
            'product.product',
            'Default Advance Product',),
    }
