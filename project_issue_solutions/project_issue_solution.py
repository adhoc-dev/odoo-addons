 #-*- coding: utf-8 -*-


from openerp.osv import fields, osv, orm

class project_isssue_solution(osv.osv):
    """ Note """
    _name = 'project.issue.solution'
    _inherit = ['mail.thread']
    _description = "Project Issue Solution"
    _order = 'name'

    _columns = {
        'name': fields.char(string='Name', required=True),
        'solution_description': fields.text('Solution Description'),
        'issue_description': fields.text('Issue Description'),
		'categ_ids': fields.many2many('project.category', string='Tags'),        
        'project_issue_ids': fields.one2many('project.issue', 'project_issue_solution_id', string='Issues'),        
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
