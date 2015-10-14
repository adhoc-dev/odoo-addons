# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, api, _
from openerp.exceptions import Warning


class project_issue(models.Model):
    _inherit = 'project.issue'

    @api.one
    @api.constrains('stage_id')
    def validate_issue(self):
        if self.task_id and self.stage_id.fold == True:
            task_open = self.env['project.task'].search(
                    [('id', '=', self.task_id.id),
                     ('stage_id.fold', '!=', True)])
            if task_open:
                raise Warning(
                    _("You can not close an issue with active task, we consider active task the one in stages without option 'folded'"))

