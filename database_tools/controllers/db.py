# -*- coding: utf-8 -*-
import openerp.http as http
# import os
import base64
from openerp import _, modules
from openerp.exceptions import Warning
from openerp.service import db as db_ws
import logging
_logger = logging.getLogger(__name__)

import simplejson
from openerp.addons.web.http import request

class RestoreDB(http.Controller):

    @http.route(
        '/restore_db',
        type='json',
        auth='none',
        # methods=['POST'],
        )
    def restore_db(self, **post):
        # import pudb; pudb.set_trace()
        print 'aaaaaaaaaaaaaaa'
        # TODO chequear admin
        # _logger.info("Restoring database %s from %s" % db_name, file_path)
        # error = False
        # try:
        #     f = file(file_path, 'r')
        #     data_b64 = base64.encodestring(f.read())
        #     f.close()
        # except Exception, e:
        #     error = (_(
        #         'Unable to read file %s\n\
        #         This is what we get: \n %s') % (
        #         file_path, e))
        # try:
        #     db_ws.exp_restore(db_name, data_b64)
        # except Exception, e:
        #     error = (_(
        #         'Unable to restore bd %s, this is what we get: \n %s') % (
        #         db_name, e))

        # # disable or enable backups
        # # TODo unificar con la que esta en database
        # registry = modules.registry.RegistryManager.get(db_name)
        # with registry.cursor() as db_cr:
        #     registry['ir.config_parameter'].set_param(
        #         db_cr, 1, 'database.backups.enable', str(backups_state))
        # print 'error', error
        # if error:
        #     return {'error': error}
        # else:
        #     return True
