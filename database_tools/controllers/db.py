# -*- coding: utf-8 -*-
import openerp.http as http
import os
import base64
from openerp import _
from openerp.exceptions import Warning
from openerp.service import db as db_ws
import logging
_logger = logging.getLogger(__name__)


class RestoreDB(http.Controller):

    @http.route(
        '/restore_db/<admin>/<file_path>/<db_name>',
        type="http",
        auth='none'
        )
    def restore_db(self, admin, file_path, db_name):
        # TODO chequear admin
        _logger.info("Restoring database %s from %s" % db_name, file_path)
        try:
            f = file(file_path, 'r')
            data_b64 = base64.encodestring(f.read())
            f.close()
        except Exception, e:
            raise Warning(_(
                'Unable to read file %s\n\
                This is what we get: \n %s') % (
                file_path, e))
        try:
            db_ws.exp_restore(db_name, data_b64)
        except Exception, e:
            raise Warning(_(
                'Unable to restore bd %s, this is what we get: \n %s') % (
                db_name, e))
