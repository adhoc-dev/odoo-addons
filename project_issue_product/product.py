# -*- coding: utf-8 -*-
from openerp.osv import fields, osv


class product_product(osv.osv):
    _inherit = 'product.product'
    _columns = {
        'project_issue_ids': fields.one2many(
            'project.issue', 'product_id', string='Issues'),
    }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
