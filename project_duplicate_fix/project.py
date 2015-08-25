# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################


from openerp import models, api


class project(models.Model):

    """"""

    _inherit = 'project.project'

    @api.one
    def copy(self, default=None):
        res = super(project, self).copy(default)
        res.message_ids.unlink()
        res.analytic_account_id.message_ids.unlink()
        return res
