# -*- coding: utf-8 -*-

# from functools import partial
import logging
# from lxml import etree
# from lxml.builder import E

import openerp
from openerp import SUPERUSER_ID
# from openerp import tools
# import openerp.exceptions
from openerp.osv import fields,osv
# from openerp.osv.orm import browse_record
from openerp.tools.translate import _

# from res_config import res_config

_logger = logging.getLogger(__name__)

#----------------------------------------------------------
# Basic res.groups and res.users
#----------------------------------------------------------

class res_users(osv.osv):
    _inherit = "res.users"
# TODO, implemetnar que cuando cambio el pass de admin o el login se actualicen los datos en catchaall

    # def write(self, cr, uid, ids, values, context=None):
    #     res = super(res_users, self).write(cr, uid, ids, values, context=context)
    #     if uid == SUPERUSER_ID and 'password' in values:
    #         set_local_alias = self.pool.get("ir.config_parameter").get_param(cr, uid, "mail.catchall.set_local_alias", context=context)
    #         if set_local_alias:
    #             self.update_local_alias(cr, uid, context=context)
    #     return res

    # def update_local_alias(self, cr, uid, context=None):
    #     settings_obj = self.pool['base.config.settings']
    #     config_parameters = self.pool.get("ir.config_parameter")
    #     alias_domain = config_parameters.get_param(cr, uid, "mail.catchall.domain", context=context)
        
    #     # Get the new local_alias
    #     local_alias = settings_obj.get_local_alias(cr, uid, alias_domain, context=context), 

    #     # Update de local_alias parameter        
    #     config_parameters.set_param(cr, uid, "mail.catchall.set_local_alias", str(local_alias) or 'False', context=context)

    #     local_alias_path = config_parameters.get_param(cr, uid, "mail.catchall.local_alias_path", context=context)
    #     if local_alias_path and alias_domain and local_alias:
    #         try:
    #             if not settings_obj.search_for_line(cr, uid, local_alias_path, alias_domain, context=context):
    #                 #  no se porque tengo error en esta funcion llamando desde aca
    #                 settings_obj.write_new_line(cr, uid, local_alias_path, local_alias, context=context)        
    #             else: 
    #                 #  no se porque tambien tengo error en esta funcion llamando desde aca
    #                 settings_obj.replace_line(cr, uid, local_alias_path, alias_domain, local_alias, context=context)
    #             settings_obj.reload_postfix(cr, uid, [], context=context)
    #         except IOError as error:
    #             print 'No file ' + error
