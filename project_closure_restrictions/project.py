# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, api, _
from openerp.exceptions import Warning


class project_project(models.Model):
    _inherit = 'project.project'

    @api.multi
    def set_done(self):
        for project in self:
            if not project.analytic_account_id.state == 'close':
                raise Warning(
                    _("You can not cancel the project if the analytic account is open"))
            if project.task_ids:
                tasks_open = project.env['project.task'].search(
                    [('id', 'in', [x.id for x in project.task_ids]), ('stage_id.fold', '!=', True)])
                if tasks_open:
                    raise Warning(
                        _("You can not close a project with active task, we consider active task the one in stages without option 'folded'"))

        return super(project_project, self).set_done()
