 #-*- coding: utf-8 -*-


from openerp.osv import fields, osv, orm

class project_issue(osv.osv):
    _inherit = 'project.issue'

    _columns = {
        'product_id': fields.many2one('product.product','Product'),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
