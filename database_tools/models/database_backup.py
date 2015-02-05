# -*- coding: utf-8 -*-
import os
import base64
from openerp import models, fields, api, _
from openerp.exceptions import Warning
from openerp.service import db as db_ws


class database_backup(models.Model):
    _name = 'db.database.backup'
    _description = 'Database Backup'
    _order = "create_date desc"

    database_id = fields.Many2one(
        'db.database',
        string='Database',
        readonly=True,
        required=True
    )
    date = fields.Datetime(
        string='Date',
        readonly=True,
        required=True
    )
    name = fields.Char(
        string='Name',
        readonly=True,
        required=True
    )
    path = fields.Char(
        string='Path',
        readonly=True,
        required=True
    )
    type = fields.Selection(
        [('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')],
        string='Type',
        required=True
    )

    @api.one
    def delete(self):
        """"""
        try:
            raise Warning(_('Not Implemented yet'))

        except SystemExit:
            raise Warning(
                _("Unable to delete database backup"))

    def download(self):
        """Descarga el back up en el exploradorador del usuario"""
        raise Warning(_('Not Implemented yet'))

    @api.one
    def restore(self, new_name, backups_enable):
        f = file(os.path.join(self.path, self.name), 'r')
        data_b64 = base64.encodestring(f.read())
        f.close()
        try:
            db_ws.exp_restore(self.name, data_b64)
        except Exception, e:
            raise Warning(_(
                'Unable to restore bd %s, this is what we get: \n %s') % (
                self.name, e))
        else:
            self.env['db.database'].backups_state(new_name, backups_enable)

    @api.multi
    def unlink(self):
        # raise Warning(_('Not Implemented yet'))
        database_path = os.path.join(self.path, self.name)
        try:
            os.remove(database_path)
        except Exception, e:
            # TODO cambiar por un alerta en log y algo en los registros
            # raise Warning(_(
                # 'Unable to remoove database file on %s, this is what we get: \n %s') % (
                # database_path, e))
            print 'error', e
        return super(database_backup, self).unlink()
