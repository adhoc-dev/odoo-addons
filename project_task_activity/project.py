# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, api, fields
from datetime import datetime


class project_task_activity(models.Model):
    _name = 'project.task.activity'

    task_id = fields.Many2one(
        'project.task',
        required=True, ondelete='cascade')
    name = fields.Char('Name', required=True)
    user_id = fields.Many2one('res.users', 'Responsible', required=True)
    planned_date = fields.Datetime('Planned Date')
    done_date = fields.Datetime('Done Date')
    state = fields.Selection(
        [('pending', 'Pending'), ('done', 'Done')],
        'State', default='pending', required=True)
    description = fields.Text('Description')

    @api.one
    def action_done(self):
        if self.state == 'pending':
            self.state = 'done'
            self.done_date = datetime.today()
        else:
            self.state = 'pending'


class project_task(models.Model):
    _inherit = 'project.task'

    activity_ids = fields.One2many(
        'project.task.activity', 'task_id', 'Activity', copy=True)
