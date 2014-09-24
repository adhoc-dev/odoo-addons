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
        'project_tag_ids': fields.many2many('project_tags.project_tag', 'project_tags___project_tag_ids_rel', 'project_id', 'project_tag_id', string='Tags'), 
    }

    _defaults = {
    }


    _constraints = [
    ]




project()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
