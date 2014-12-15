# -*- coding: utf-8 -*-
from openerp import models, fields, api, _


class task(models.Model):
    _inherit = 'project.task'

    user_story = fields.Boolean(
        'Is User Story?',
        default=False)

    @api.multi
    def action_open_task(self):
        print 'context', self._context
        return {
            'name': _('User Story'),
            'view_type': 'form',
            'view_mode': 'form',
            # 'view_id': [res_id],
            'res_model': 'project.task',
            'context': self._context,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current',
            'res_id': self.id,
        }


class project(models.Model):
    _inherit = 'project.project'

    user_story_ids = fields.One2many(
        'project.task',
        'project_id',
        domain=[('user_story', '=', True)],
        context={'default_user_story': True},
        string='User Stories',
    )
