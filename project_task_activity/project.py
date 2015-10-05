# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, api, fields, _
from datetime import datetime
import json


class project_task_activity(models.Model):
    _name = 'project.task.activity'
    _order = "sequence"

    task_id = fields.Many2one(
        'project.task',
        string='Task',
        required=True, ondelete='cascade')
    project_id = fields.Many2one(
        'project.project',
        string='Project',
        related='task_id.project_id', readonly=True, store=True)
    name = fields.Char('Name', required=True)
    user_id = fields.Many2one('res.users', 'Responsible')
    planned_date = fields.Datetime('Planned Date')
    done_date = fields.Datetime('Done Date')
    state = fields.Selection(
        [('pending', 'Pending'), ('done', 'Done'), ('cancel', 'Cancel')],
        'State', default='pending', required=True)
    description = fields.Text('Description')
    sequence = fields.Integer(
        'Sequence',
        help="Gives the sequence order when selecting an activitiy.",
        default=10)

    @api.one
    def action_done(self):
        if self.state == 'pending':
            self.state = 'done'
            self.done_date = datetime.today()
        else:
            self.state = 'pending'
            self.done_date = False

    @api.one
    def action_cancel(self):
        self.state = 'cancel'


class project_task(models.Model):
    _inherit = 'project.task'

    activity_ids = fields.One2many(
        'project.task.activity', 'task_id', 'Activity', copy=True)
    activities_progress = fields.Char(
        string=_("Progress"),
        compute='_get_activities_progress')

    @api.one
    @api.depends('activity_ids.state')
    def _get_activities_progress(self):
        res = []
        for activity in self.activity_ids:
            if activity.state == 'done':
                res.insert(0, {'tooltip': activity.name, 'value': 1})
            elif activity.state != 'cancel':
                res.insert(0, {'tooltip': activity.name, 'value': 0})
        self.activities_progress = json.dumps(res)


class project_project(models.Model):
    _inherit = 'project.project'

    activity_ids = fields.One2many(
        'project.task.activity',
        string='Activity', compute='_get_task_activity')
    activities_todo = fields.Float(
        string='Activities to do', compute='_get_activities_todo')
    activities_done = fields.Float(
        string='Activities done', compute='_get_activities_done')
    progress_activities = fields.Float(
        string=_("Progress"),
        compute='_get_progress_activities')

    @api.one
    def _get_task_activity(self):
        self.activity_ids = self.env['project.task.activity'].search(
            [('project_id', '=', self.id)])

    @api.one
    def _get_activities_todo(self):
        self.activities_todo = len(
            self.activity_ids.filtered(lambda x: x.state != 'cancel'))

    @api.one
    def _get_activities_done(self):
        self.activities_done = len(
            self.activity_ids.filtered(lambda x: x.state == 'done'))

    @api.one
    def _get_progress_activities(self):
        self.progress_activities = 0
        if self.activity_ids:
            if self.activities_todo != 0:
                self.progress_activities = round(
                    100 * (self.activities_done / self.activities_todo), 1)
