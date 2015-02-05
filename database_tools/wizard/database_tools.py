# -*- encoding: utf-8 -*-
from openerp import models, fields, api


class db_database_tools_wizard(models.TransientModel):
    _name = 'db.database.tools.wizard'

    name = fields.Char('New Database Name', size=64, required=True)
    action_type = fields.Char('Action Type', required=True)
    backups_enable = fields.Boolean('Backups Enable on new DB?')

    @api.multi
    def action_confirm(self):
        active_id = self._context.get('active_id')
        active_model = self._context.get('active_model')
        if not active_id or not active_model:
            return False
        active_record = self.env[active_model].browse(active_id)
        if self.action_type == 'duplicate':
            active_record.duplicate(self.name, self.backups_enable)
        elif self.action_type == 'restore':
            active_record.restore(self.name, self.backups_enable)
