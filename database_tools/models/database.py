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

    @api.one
    def action_backups_state(self):
        self.backups_state(self.name, True)

    @api.model
    def backups_state(self, db_name, type):
        registry = modules.registry.RegistryManager.get(db_name)
        with registry.cursor() as db_cr:
            # registry['ir.config_parameter'].init(db_cr, force=True)
            # TODO ver si mejor desactivamos modificando el cron
            registry['ir.config_parameter'].set_param(
                db_cr, 1, 'prueba.prueba', 'aaaaaaaasdasdasdaaaa')
        return True

    @api.one
    def duplicate(self, new_name, backups_enable):
        # TODO poner un warning o algo de que si se duplica la bd actual se
        # arroja un warning, ver si lo podemos controlar
        # (porque se cierran las conexiones)
        try:
            db_ws.exp_duplicate_database(self.name, new_name)
        except Exception, e:
            raise Warning(_(
                'Unable to duplicate bd %s, this is what we get: \n %s') % (
                self.name, e))
        else:
            self.backups_state(new_name, backups_enable)

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
        # TODO log diciendo running backup_type backups
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
    def database_backup_clean(self, type='daily'):
        current_date = time.strftime('%Y-%m-%d')
        from_date = datetime.strptime(current_date, '%Y-%m-%d')
        if type == 'daily':
            interval = self.daily_save_periods
            from_date = from_date+relativedelta(days=-interval)
        elif type == 'weekly':
            interval = self.weekly_save_periods
            from_date = from_date+relativedelta(weeks=-interval)
        elif type == 'monthly':
            interval = self.monthly_save_periods
            from_date = from_date+relativedelta(months=-interval)

        from_date = from_date.strftime('%Y-%m-%d')
        databases = self.env['db.database.backup'].search([
            ('database_id', '=', self.id),
            ('type', '=', type),
            ('date', '<=', from_date),
            ])
        for database in databases:
            database.unlink()

    @api.one
    def database_backup(self, type='daily'):
        now = datetime.now()

        # check if bd exists
        try:
            if not db_ws.exp_db_exist(self.name):
                # TODO escribir en el log
                print 'no existe'
        except:
            raise
            # TODO escribir en el log

        # verificar o crear path para backups
        try:
            # TODO escribir en el log
            if not os.path.isdir(self.backups_path):
                os.makedirs(self.backups_path)
        except:
            # TODO escribir en el log
            raise

        # TODO agregar monthly o lo que sea al nombre
        backup_name = '%s_%s_%s.zip' % (
            self.name, type, now.strftime('%Y%m%d_%H%M%S'))
        backup_path = os.path.join(self.backups_path, backup_name)
        backup = open(backup_path, 'wb')

        # backup
        try:
            backup.write(base64.b64decode(
                db_ws.exp_dump(self.name)))
        except:
            # TODO escribir en el log
            raise Warning(
                _('Unable to dump Database. If you are working in an \
                    instance with "workers" then you can try \
                    restarting service.'))
        else:
            backup.close()
            self.backup_ids.create({
                'database_id': self.id,
                'name': backup_name,
                'path': self.backups_path,
                'date': now,
                'type': type,
                })
        # TODO analizar si hacemos como en los contratos
        # next_date = datetime.datetime.strptime(
            # contract.recurring_next_date or current_date, "%Y-%m-%d")
        current_date = time.strftime('%Y-%m-%d')
        next_date = datetime.strptime(current_date, '%Y-%m-%d')
        interval = 1
        # next_date = datetime.datetime.strptime(
            # contract.recurring_next_date or current_date, "%Y-%m-%d")
        if type == 'daily':
            new_date = next_date+relativedelta(days=+interval)
            self.daily_next_date = new_date
        elif type == 'weekly':
            new_date = next_date+relativedelta(weeks=+interval)
            self.weekly_next_date = new_date
        elif type == 'monthly':
            new_date = next_date+relativedelta(months=+interval)
            self.monthly_next_date = new_date
            # logger.notifyChannel(
                # 'backup', netsvc.LOG_INFO,
                # "Could'nt backup database %s. Bad database administrator password for server running at http://%s:%s" %(rec.name, rec.host, rec.port))

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
