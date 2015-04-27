# -*- coding: utf-8 -*-
import os
from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)


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
    full_path = fields.Char(
        string='Path',
        compute='get_full_path',
    )
    type = fields.Selection(
        [('manual', 'Manual'), ('daily', 'Daily'),
         ('weekly', 'Weekly'), ('monthly', 'Monthly')],
        string='Type',
        required=True
    )

    @api.one
    @api.depends('path', 'name')
    def get_full_path(self):
        self.full_path = os.path.join(self.path, self.name)

    @api.multi
    def unlink(self):
        for backup in self:
            try:
                os.remove(backup.full_path)
            except Exception, e:
                _logger.warning(
                    'Unable to remoove database file on %s, this is what we get:\
                    \n %s' % (backup.full_path, e.strerror))
        return super(database_backup, self).unlink()
