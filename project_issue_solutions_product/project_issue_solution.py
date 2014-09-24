 #-*- coding: utf-8 -*-


from openerp.osv import fields, osv, orm

class project_isssue_solution(osv.osv):
    """ Note """
    _inherit = 'project.issue.solution'

    _columns = {
		'product_ids': fields.many2many('product.product', 'project_issue_solution_product_rel', 'solution_id','product_id', string='Products'),        
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
