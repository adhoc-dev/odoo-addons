# -*- coding: utf-8 -*-
from openerp import models, fields


class project_type(models.Model):

    _name = 'project.stage'
    _description = 'Project Stage'
    _order = 'sequence'

    name = fields.Char('Stage Name', required=True, translate=True)
    description = fields.Text('Description')
    sequence = fields.Integer('Sequence')
    case_default = fields.Boolean(
        'Default for New Projects',
        help="If you check this field, this stage will be proposed by default on each new project. It will not assign this stage to existing projects.")
    fold = fields.Boolean(
        'Folded in Kanban View',
        help='This stage is folded in the kanban view when'
        'there are no records in that stage to display.')


class project(models.Model):

    _inherit = 'project.project'

    stage_id = fields.Many2one(
        'project.stage',
        'Stage',
        track_visibility='onchange',
        select=True,
        copy=False)
    kanban_state = fields.Selection(
        [('normal', 'In Progress'), ('blocked', 'Blocked'),
         ('done', 'Ready for next stage')],
        'Kanban State',
        track_visibility='onchange',
        help="A task's kanban state indicates special situations affecting it:\n"
        " * Normal is the default situation\n"
        " * Blocked indicates something is preventing the progress of this task\n"
        " * Ready for next stage indicates the task is ready to be pulled to the next stage",
        required=False,
        copy=False)

    _order = "sequence"
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
