# -*- coding: utf-8 -*-
##############################################################################
#
#    Projects related projects
#    Copyright (C) 2013 Sistemas ADHOC
#    No email
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


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
