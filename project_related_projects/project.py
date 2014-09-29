# -*- coding: utf-8 -*-



import re
from openerp import netsvc
from openerp.osv import osv, fields

class project(osv.osv):
    """"""
    
    _name = 'project.project'
    _inherits = {  }
    _inherit = [ 'project.project' ]

    _columns = {
        'related_to_ids': fields.many2many('project.project', 'project_project_related_rel', 'project_id', 'related_to_id', 'Related To Projects'),
        'related_by_ids': fields.many2many('project.project', 'project_project_related_rel', 'related_to_id', 'project_id', 'Related By Projects'),

#        'parent_ids': fields.many2many('project.project', 'project_project_parent_rel', 'project_id', 'parent_id', 'Parent Projects'),
#        'child_ids': fields.many2many('project.project', 'project_project_parent_rel', 'parent_id', 'project_id', 'Delegated Project'),
#        'realated_project_ids': fields.many2many('project.project', 'project_related_projects_realated_project_ids_project_related_ids_rel', 'project_id', 'project_id', string='Related Project'), 
    }

    _defaults = {
    }


    _constraints = [
    ]




project()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
