# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-today OpenERP SA (<http://www.openerp.com>)
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

from openerp.osv import fields, osv
from openerp.tools.translate import _

class project_task_type(osv.osv):
    _name = 'project.task.phase'
    _description = 'Task Phase'
    _order = 'sequence'
    _columns = {
        'name': fields.char('Phase Name', required=True, size=64, translate=True),
        'sequence': fields.integer('Sequence'),
    }

class task(osv.osv):
    _inherit = 'project.task'    
    _columns = {
        'phase_id': fields.many2one('project.task.phase', 'Phase',),
    }    