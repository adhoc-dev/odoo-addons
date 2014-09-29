# -*- coding: utf-8 -*-


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