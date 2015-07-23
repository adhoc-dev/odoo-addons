# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api, _

WARNING_TYPES = [
    ('warning', 'Warning'), ('info', 'Information'), ('error', 'Error')]


class warning_box(models.TransientModel):
    _name = 'warning_box'
    _description = 'warning_box'
    _req_name = 'title'

    type = fields.Selection(
        WARNING_TYPES,
        string='Type',
        readonly=True
        )
    title = fields.Char(
        string="Title",
        size=100,
        readonly=True
        )
    message = fields.Text(
        string="Message",
        readonly=True
        )

    @api.multi
    def message_action(self):
        self.ensure_one
        message_type = [t[1]for t in WARNING_TYPES if self.type == t[0]][0]
        res = {
            'name': '%s: %s' % (_(message_type), _(self.title)),
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env['ir.model.data'].xmlid_to_res_id(
                'warning_box.warning_box_form'),
            'res_model': 'warning_box',
            'domain': [],
            'context': self._context,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': self.id
        }
        return res

    @api.model
    def warning(self, title, message):
        record = self.create({
            'title': title,
            'message': message,
            'type': 'warning'})
        return record.message_action()

    @api.model
    def info(self, title, message):
        record = self.create({
            'title': title,
            'message': message,
            'type': 'info'})
        return record.message_action()

    @api.model
    def error(self, title, message):
        record = self.create({
            'title': title,
            'message': message,
            'type': 'info'})
        return record.message_action()
