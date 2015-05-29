# -*- coding: utf-8 -*-
from openerp import models, api, _
from openerp.exceptions import Warning


class project(models.Model):
    _inherit = 'project.project'

    @api.one
    def set_done(self):
        if not self.analytic_account_id.state == 'close':
            raise Warning(
                _("You can not cancel the project if the analytic account is open"))
        if self.task_ids:
            tasks_open = self.env['project.task'].search(
                [('id', 'in', [x.id for x in self.task_ids]), ('stage_id.fold', '!=', True)])
            if tasks_open:
                raise Warning(
                    _("You can not close a project with active task, we consider active task the one in stages without option 'folded'"))

        return super(project, self).set_done()
