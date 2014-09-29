# -*- coding: utf-8 -*-



import re
from openerp import netsvc
from openerp.osv import osv, fields

class project_tag(osv.osv):
    """"""
    
    _name = 'project_tags.project_tag'
    _description = 'project_tag'

    _columns = {
        'name': fields.char(string='Name', required=True, size=64),
        'project_id': fields.many2many('project.project', 'project_tags___project_tag_ids_rel', 'project_tag_id', 'project_id', string='&lt;no label&gt;'), 
    }

    _defaults = {
    }


    _constraints = [
    ]




project_tag()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
