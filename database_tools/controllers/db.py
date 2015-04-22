# -*- coding: utf-8 -*-
import openerp.http as http
import base64
from openerp import _, modules
from openerp.service import db as db_ws
from fabric.api import env
from fabric.operations import get
import os
import logging
_logger = logging.getLogger(__name__)


class RestoreDB(http.Controller):

    @http.route(
        '/restore_db',
        type='json',
        auth='none',
        )
    def restore_db(
            self, admin_pass, db_name, file_path, file_name,
            backups_state, remote_server=False):
        database_file = os.path.join(file_path, file_name)
        if remote_server:
            local_path = '/opt/odoo/backups/tmp/'
            user_name = remote_server.get('user_name')
            password = remote_server.get('password')
            host_string = remote_server.get('host_string')
            port = remote_server.get('port')
            if not user_name or not password or not host_string or not port:
                return {'error': 'You need user_name, password, host_string\
                and port in order to use remote_server'}
            env.user = user_name
            env.password = password
            env.host_string = host_string
            env.port = port
            _logger.info("Getting file '%s' from '%s:%s' with user %s" % (
                database_file, host_string, port, user_name))
            res = get(remote_path=database_file, local_path=local_path, use_sudo=True)
            if not res.succeeded:
                return {'error': 'Could not copy file from remote server'}
            database_file = os.path.join(local_path, file_name)

        _logger.info("Restoring database %s from %s" % (db_name, database_file))
        error = False
        try:
            _logger.info("Reading file for restore")
            f = file(database_file, 'r')
            data_b64 = base64.encodestring(f.read())
            f.close()
        except Exception, e:
            error = (_(
                'Unable to read file %s\n\
                This is what we get: \n %s') % (
                database_file, e))
            return {'error': error}
        try:
            _logger.info("Restoring....")
            db_ws.exp_restore(db_name, data_b64)
        except Exception, e:
            error = (_(
                'Unable to restore bd %s, this is what we get: \n %s') % (
                db_name, e))
            return {'error': error}

        _logger.info("Databse %s restored succesfully!" % db_name)
        # # disable or enable backups
        # TODO unificar con la que esta en database
        registry = modules.registry.RegistryManager.get(db_name)
        _logger.info("Disable/Enable Backups on %s!" % db_name)
        with registry.cursor() as db_cr:
            registry['ir.config_parameter'].set_param(
                db_cr, 1, 'database.backups.enable', str(backups_state))
        return {}
