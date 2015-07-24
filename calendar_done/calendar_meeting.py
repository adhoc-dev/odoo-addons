# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models, api
from openerp.tools.translate import _
from openerp.exceptions import Warning


class meeting(models.Model):
    _inherit = "calendar.event"

    mark_done = fields.Boolean(string='Mark As Done')
    previous_user_id = fields.Many2one('res.users', string='Previous User')

    @api.onchange('mark_done')
    def on_change_mark_done(self):
        company = self.env['res.users'].browse(self._uid).company_id
        if not company.calendar_mark_done_user_id:
            raise Warning(
                _('You should set the mark done user on the company!'))
        if self.mark_done:
            self.previous_user_id = self.user_id.id
            self.user_id = company.calendar_mark_done_user_id.id
        else:
            self.user_id = self.previous_user_id.id
            self.previous_user_id = False
