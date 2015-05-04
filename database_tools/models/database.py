# -*- encoding: utf-8 -*-
import xmlrpclib
import os
import base64
from datetime import datetime
from openerp import fields, models, api, _, modules
from openerp.exceptions import Warning
from openerp.tools import config
from openerp.service import db as db_ws
from dateutil.relativedelta import relativedelta
import time
import logging
_logger = logging.getLogger(__name__)
# TODO una buena forma generica de ejecutar metodos y devolver errores
# def execute(connector, method, *args):
#     res = False
#     try:        
#         res = getattr(connector,method)(*args)
#     except socket.error,e:        
#             raise e
#     return res
# Luego se usa
# bkp = execute(conn, 'dump', tools.config['admin_passwd'], rec.name)


class db_database(models.Model):

    """Ver si podemos presindir de host y port y nos conectamos siempre a la instancia en la cual estamos,
    probar si podemos ir directo a los ws o si necesitamos los datos los leemos con campos funcion
    """
    _name = 'db.database'

    @api.model
    def _get_default_port(self):
        if config['xmlrpcs'] and config['xmlrpcs_port']:
            return config['xmlrpcs_port']
        elif config['xmlrpc'] and config['xmlrpc_port']:
            return config['xmlrpc_port']
        else:
            return False

    @api.model
    def _get_default_name(self):
        return self._cr.dbname

    not_self_name = fields.Char(
        'Database',
        default=_get_default_name,
    )
    name = fields.Char(
        'Database',
        compute='_get_name',
    )
    type = fields.Selection(
        [('self', 'Self'), ('local', 'Local'), ('remote', 'Remote')],
        string='Type',
        required=True,
        default='self',
    )
    host = fields.Char(
        'Host',
        default='localhost',
    )
    admin_pass = fields.Char(
        'Admin Pass',
    )
    port = fields.Integer(
        'Port',
        default=_get_default_port,
    )
    backups_path = fields.Char(
        string='Backups Path',
        required=True,
        default='/var/odoo/backups/',
        help='User running this odoo intance must have CRUD access rights on this folder'
        # TODO agregar boton para probar que se tiene permisos
    )
    daily_backup = fields.Boolean(
        string='Daily Backups?',
    )
    weekly_backup = fields.Boolean(
        string='Weekly Backups?',
    )
    monthly_backup = fields.Boolean(
        string='Monthly Backups?',
    )
    daily_next_date = fields.Date(
        string='Daily Next Date',
        default=fields.Date.context_today,
        required=True,
    )
    weekly_next_date = fields.Date(
        string='Weekly Next Date',
        default=fields.Date.context_today,
        required=True,
    )
    monthly_next_date = fields.Date(
        string='Monthly Next Date',
        default=fields.Date.context_today,
        required=True,
    )
    daily_save_periods = fields.Integer(
        string='Daily Save Periods',
        default=7,
        required=True,
    )
    weekly_save_periods = fields.Integer(
        string='Weekly Save Periods',
        default=4,
        required=True,
    )
    monthly_save_periods = fields.Integer(
        string='Monthly Save Periods',
        default=12,
        required=True,
    )
    backup_ids = fields.One2many(
        'db.database.backup',
        'database_id',
        string='Backups',
        readonly=True,
    )
    backup_count = fields.Integer(
        string='# Backups',
        compute='_get_backups'
    )

    @api.one
    @api.depends('type', 'not_self_name')
    def _get_name(self):
        name = self.not_self_name
        if self.type == 'self':
            name = self._cr.dbname
        self.name = name

    @api.one
    @api.depends('backup_ids')
    def _get_backups(self):
        self.backup_count = len(self.backup_ids)

    @api.model
    def backups_state(self, db_name, state_type):
        registry = modules.registry.RegistryManager.get(db_name)
        with registry.cursor() as db_cr:
            registry['ir.config_parameter'].set_param(
                db_cr, 1, 'database.backups.enable', str(state_type))
        return True

    @api.multi
    def update_backups_data(self):
        self.ensure_one()
        for backup in self.backup_ids:
            if not os.path.isfile(backup.full_path):
                backup.unlink()
        return True

    @api.multi
    def drop_con(self):
        self.ensure_one()
        db_ws._drop_conn(self._cr, self.name)
        # Por si no anda...
        # db = sql_db.db_connect('postgres')
        # with closing(db.cursor()) as pg_cr:
        #     pg_cr.autocommit(True)     # avoid transaction block
        #     db_ws._drop_conn(pg_cr, self.name)
        return True

    @api.multi
    def get_sock(self):
        self.ensure_one()
        base_url = self.host
        server_port = self.port
        rpc_db_url = 'http://%s:%d/xmlrpc/db' % (base_url, server_port)
        # TODO implementar en las distintas funciones, tal vez mejor hacer como
        # un parser generico
        # example of use
        # sock = self.get_sock()
        # if not sock.db_exist(self.name):
        return xmlrpclib.ServerProxy(rpc_db_url)

    @api.one
    @api.constrains('type')
    def _check_type(self):
        if self.type == 'remote':
            raise Warning(_('Type Remote not implemented yet'))

    @api.one
    @api.constrains('type', 'not_self_name')
    def _check_db_exist(self):
        if self.type != 'self' and not db_ws.exp_db_exist(self.not_self_name):
            raise Warning(_('Database %s do not exist') % (self.not_self_name))

    @api.model
    def cron_database_backup(self):
        backups_enable = self.env['ir.config_parameter'].get_param(
                'database.backups.enable')
        if backups_enable != 'True':
            _logger.warning('Backups are disable. If you want to enable it you should add the parameter database.backups.enable with value True')
            return False
        _logger.info('Running backups cron')
        current_date = time.strftime('%Y-%m-%d')
        daily_databases = self.search([
            ('daily_backup', '=', True),
            ('daily_next_date', '<=', current_date),
            ])
        daily_databases.database_backup('daily')
        weekly_databases = self.search([
            ('weekly_backup', '=', True),
            ('weekly_next_date', '<=', current_date),
            ])
        weekly_databases.database_backup('weekly')
        monthly_databases = self.search([
            ('monthly_backup', '=', True),
            ('monthly_next_date', '<=', current_date),
            ])
        monthly_databases.database_backup('monthly')
        # clean databases
        databases = self.search([])
        databases.database_backup_clean('daily')
        databases.database_backup_clean('weekly')
        databases.database_backup_clean('monthly')

    @api.one
    def database_backup_clean(self, bu_type='daily'):
        current_date = time.strftime('%Y-%m-%d')
        from_date = datetime.strptime(current_date, '%Y-%m-%d')
        if bu_type == 'daily':
            interval = self.daily_save_periods
            from_date = from_date+relativedelta(days=-interval)
        elif bu_type == 'weekly':
            interval = self.weekly_save_periods
            from_date = from_date+relativedelta(weeks=-interval)
        elif bu_type == 'monthly':
            interval = self.monthly_save_periods
            from_date = from_date+relativedelta(months=-interval)

        from_date = from_date.strftime('%Y-%m-%d')
        databases = self.env['db.database.backup'].search([
            ('database_id', '=', self.id),
            ('type', '=', bu_type),
            ('date', '<=', from_date),
            ])
        for database in databases:
            database.unlink()

    @api.one
    def action_database_backup(self):
        """Action to be call from buttons"""
        self.ensure_one()
        return self.database_backup('manual')

    @api.multi
    def database_backup(self, bu_type):
        self.ensure_one()
        now = datetime.now()

        # check if bd exists
        try:
            if not db_ws.exp_db_exist(self.name):
                error = "Database %s do not exist" % (self.name)
                _logger.warning(error)
                return {'error': error}
        except Exception, e:
            error = "Could not check if database %s exists. This is what we get:\n\
                %s" % (self.name, e)
            _logger.warning(error)
            return {'error': error}

        # crear path para backups si no existe
        try:
            if not os.path.isdir(self.backups_path):
                os.makedirs(self.backups_path)
        except Exception, e:
            error = "Could not create folder %s for backups.\
                This is what we get:\n\
                %s" % (self.backups_path, e)
            _logger.warning(error)
            return {'error': error}

        backup_name = '%s_%s_%s.zip' % (
            self.name, bu_type, now.strftime('%Y%m%d_%H%M%S'))
        backup_path = os.path.join(self.backups_path, backup_name)
        backup = open(backup_path, 'wb')

        # backup
        try:
            backup.write(base64.b64decode(
                db_ws.exp_dump(self.name)))
        except:
            error = 'Unable to dump Database. If you are working in an\
                    instance with "workers" then you can try \
                    restarting service.'
            _logger.warning(error)
            return {'error': error}
        else:
            backup.close()
            self.backup_ids.create({
                'database_id': self.id,
                'name': backup_name,
                'path': self.backups_path,
                'date': now,
                'type': bu_type,
                })

        current_date = time.strftime('%Y-%m-%d')
        next_date = datetime.strptime(current_date, '%Y-%m-%d')
        interval = 1
        if bu_type == 'daily':
            new_date = next_date+relativedelta(days=+interval)
            self.daily_next_date = new_date
        elif bu_type == 'weekly':
            new_date = next_date+relativedelta(weeks=+interval)
            self.weekly_next_date = new_date
        elif bu_type == 'monthly':
            new_date = next_date+relativedelta(months=+interval)
            self.monthly_next_date = new_date
        _logger.info('Backup %s Created' % backup_name)
        return {'backup_name': backup_name}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
