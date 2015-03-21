# -*- coding: utf-8 -*-
# from openerp import route
# from openerp import http
# import openerp
# from openerp.addons.web.controllers import main
import openerp.http as http
# from openerp.http import request
import os
import base64
# from openerp import models, fields, api, _
from openerp.exceptions import Warning
from openerp.service import db as db_ws


class RestoreDB(http.Controller):

    @http.route('/restore_db/<admin>/<file_path>/<db_name>', type="http", auth='public')
    def restore_db(self, file_path, db_name):
        # TODO chequear admin
        print 11111111111111
        print file_path
        print db_name
        print 11111111111111
        f = file(os.path.join(file_path, db_name), 'r')
        data_b64 = base64.encodestring(f.read())
        f.close()
        try:
            db_ws.exp_restore(db_name, data_b64)
        except Exception, e:
            raise Warning(_(
                'Unable to restore bd %s, this is what we get: \n %s') % (
                db_name, e))
        # return {"sample_dictionary": "This is a sample JSON dictionary"}
        # return False

# import openerp

# class dbjuan(openerp.service.db):
#     def asdas(asda):
#         print '1111'
# #     print '2222222222222'
# #     print '2222222222222'