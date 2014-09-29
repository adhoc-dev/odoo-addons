# -*- coding: utf-8 -*-


import urlparse

from openerp.osv import osv, fields
from openerp.tools.config import config as system_base_config
from openerp import SUPERUSER_ID
from openerp.addons import mail
from openerp.tools.translate import _
import os

class mail_configuration(osv.TransientModel):
    _inherit = 'base.config.settings'

    _columns = {
        'config_local_alias' : fields.boolean('Set Local Alias',),
        'virtual_alias_path':fields.char('Virtual Alias Path',),
        'virtual_alias':fields.char('Virtual Alias',),
        'local_alias_path':fields.char('Local Alias Path',),
        'local_alias' : fields.char('Local Alias',),
        'overwrite' : fields.boolean('Over Write Line',),
    }

    def on_change_alias_domain(self, cr, uid, ids, alias_domain,context=None):
        context = context or {}
        ret = {}
        if not alias_domain:
            value = {
                'local_alias': False, 
                'virtual_alias': False, 
                }   
        else:
            value = {
                'local_alias': self.get_local_alias(cr, uid, alias_domain, context=context), 
                'virtual_alias': self.get_virtual_alias(cr, uid, alias_domain, context=context), 
                }              
        return {'value': value}

    def write_virtual_alias(self, cr, uid, ids, context=None):
        alias = self.pool.get("ir.config_parameter").get_param(cr, uid, "mail.catchall.domain", context=context)
        for record in self.browse(cr, uid, ids, context=context):
            virtual_alias_path = record.virtual_alias_path
            virtual_alias = record.virtual_alias
            overwrite = record.overwrite or False
            self.write_line(cr, uid, virtual_alias_path, alias, virtual_alias, overwrite, context=context)
        raise osv.except_osv(_('Ok!'), _('File writed ok!'))

    def write_local_alias(self, cr, uid, ids, context=None):
        alias = self.pool.get("ir.config_parameter").get_param(cr, uid, "mail.catchall.domain", context=context)
        for record in self.browse(cr, uid, ids, context=context):
            local_alias_path = record.local_alias_path
            local_alias = record.local_alias
            overwrite = record.overwrite or False
            self.write_line(cr, uid, local_alias_path, alias, local_alias, overwrite, context=context)
        raise osv.except_osv(_('Ok!'), _('File writed ok!'))

    def reload_postfix(self, cr, uid, ids, context=None):
        # try:
        os.system('postmap /etc/postfix/virtual_aliases')
        os.system('newaliases')
        os.system('sudo /etc/init.d/postfix restart')
        # except IOError:
            

    def write_line(self, cr, uid, file_path, search_text, text, overwrite=False, context=None):
        """This function add or replace a line in a file
        Parameters:
            - file_path: path for the file
            - search_text: text that will be searched
            - text: text that will be written
            - overwrite: By default false, defines if a lines founded if it should be overwritten or not
        How it works:
            - if search_text is not found it will add the text at bootom
            - if search_text and overwrite = False is found it will raise and excepection
            - if search_text and overwrite = False it will recreate the file without this line and adding text at bottom
            """
        if self.search_for_line(cr, uid, file_path, text, context=context):
            raise osv.except_osv(_('Error!'), _('There is already a line with this data: %s') %(text))
        if not self.search_for_line(cr, uid, file_path, search_text, context=context):
            self.write_new_line(cr, uid, file_path, text, context=context)        
        elif overwrite:
            self.replace_line(cr, uid, file_path, search_text, text, context=context)
        else:
            raise osv.except_osv(_('Error!'), _('There is already a line for this alias %s!') %(search_text))

    def replace_line(self, cr, uid, file_path, search_text, text, context=None):
        try:
            temp_file = open(file_path, 'r')
        except IOError as error:
            print 'No file ' + error
        else:
            new_lines = []
            for line in temp_file.readlines():
                if search_text in line:
                    new_lines.append(text)
                else:
                    new_lines.append(line)
            temp_file.close()
            try:
                new_file = open(file_path, "w")
            except IOError as error:
                print 'No file ' + error                
            # else:
            #     for line in new_lines:
            #         new_file.write(line)
            #         new_file.close()
        return True

    def write_new_line(self, cr, uid, file_path, text, context=None):
        try:
            temp_file = open(file_path, 'a')
        except IOError:
            raise osv.except_osv(_('Error!'), _('File could not be writed!',))            
        else:
            temp_file.write('\n' + text)
            temp_file.close()

    def search_for_line(self, cr, uid, file_path, text, context=None):
        try:
            temp_file = open(file_path, 'r')
        except IOError:
            raise osv.except_osv(_('Error!'), _('File not found!',))
        else:
            for line in temp_file.readlines():
                if text in line:
                    temp_file.close()
                    return True
            temp_file.close()
        return False

    def get_local_alias(self, cr, uid, alias_domain, context=None):
        port = system_base_config.get('xmlrpc_port', False)
        xmlrpc = system_base_config.get('xmlrpc', False)
        mailgate_file = os.path.dirname(mail.__file__) + '/static/scripts/openerp_mailgate.py'
        admin_user = self.pool['res.users'].browse(cr, uid, SUPERUSER_ID, context=context)
        
        if not xmlrpc or not port:
            port = system_base_config.get('xmlrpcs_port', False)
            xmlrpcs = system_base_config.get('xmlrpcs', False)
            if not xmlrpcs or not port:
                print 'errror!!! falta el puerto'
        local_alias = (alias_domain or '')
        local_alias += ': "| '
        # local_alias = cr.dbname + ': "| '
        local_alias += mailgate_file
        local_alias += " --host=localhost"
        local_alias += " --port=" + str(port)
        local_alias += " -u " + str(SUPERUSER_ID)
        local_alias += " -p " + admin_user.password
        local_alias += " -d " + cr.dbname + '"'
        return local_alias

    def get_virtual_alias(self, cr, uid, alias_domain, context=None):
        return '@' + (alias_domain or '') + ' ' + (alias_domain or '') + '@localhost'

# set_local_alias
    def get_default_config_local_alias(self, cr, uid, ids, context=None):
        config_local_alias = self.pool.get("ir.config_parameter").get_param(cr, uid, "mail.catchall.config_local_alias", context=context)
        print 'config_local_alias', config_local_alias
        if not config_local_alias:
            config_local_alias = 'False'
        return {'config_local_alias': eval(config_local_alias)}

    def set_local_config_local_alias(self, cr, uid, ids, context=None):
        config_parameters = self.pool.get("ir.config_parameter")
        for record in self.browse(cr, uid, ids, context=context):
            config_parameters.set_param(cr, uid, "mail.catchall.config_local_alias", str(record.config_local_alias) or 'False', context=context)

# local_alias
    def get_default_local_alias(self, cr, uid, ids, context=None):
        local_alias = self.pool.get("ir.config_parameter").get_param(cr, uid, "mail.catchall.local_alias", context=context)
        alias_domain = self.pool.get("ir.config_parameter").get_param(cr, uid, "mail.catchall.domain", context=context)
        if not local_alias:
            local_alias = self.get_local_alias(cr, uid, alias_domain, context=context)
        return {'local_alias': local_alias}

    def set_local_alias(self, cr, uid, ids, context=None):
        config_parameters = self.pool.get("ir.config_parameter")
        for record in self.browse(cr, uid, ids, context=context):
            config_parameters.set_param(cr, uid, "mail.catchall.local_alias", record.local_alias or '', context=context)

# local_alias_path
    def get_default_local_alias_path(self, cr, uid, ids, context=None):
        local_alias_path = self.pool.get("ir.config_parameter").get_param(cr, uid, "mail.catchall.local_alias_path", context=context)
        if not local_alias_path:
            local_alias_path = "/etc/aliases"
        return {'local_alias_path': local_alias_path}

    def set_local_alias_path(self, cr, uid, ids, context=None):
        config_parameters = self.pool.get("ir.config_parameter")
        for record in self.browse(cr, uid, ids, context=context):
            config_parameters.set_param(cr, uid, "mail.catchall.local_alias_path", record.local_alias_path or '', context=context)

# virtual_alias_path
    def get_default_virtual_alias_path(self, cr, uid, ids, context=None):
        virtual_alias_path = self.pool.get("ir.config_parameter").get_param(cr, uid, "mail.catchall.virtual_alias_path", context=context)
        if not virtual_alias_path:
            virtual_alias_path = "/etc/postfix/virtual_aliases"
        return {'virtual_alias_path': virtual_alias_path}

    def set_virtual_alias_path(self, cr, uid, ids, context=None):
        config_parameters = self.pool.get("ir.config_parameter")
        for record in self.browse(cr, uid, ids, context=context):
            config_parameters.set_param(cr, uid, "mail.catchall.virtual_alias_path", record.virtual_alias_path or '', context=context)

# virtual_alias
    def get_default_virtual_alias(self, cr, uid, ids, context=None):
        virtual_alias = self.pool.get("ir.config_parameter").get_param(cr, uid, "mail.catchall.virtual_alias", context=context)
        alias_domain = self.pool.get("ir.config_parameter").get_param(cr, uid, "mail.catchall.domain", context=context)
        if not virtual_alias:
            virtual_alias = self.get_virtual_alias(cr, uid, alias_domain, context=context)
        return {'virtual_alias': virtual_alias}

    def set_virtual_alias(self, cr, uid, ids, context=None):
        config_parameters = self.pool.get("ir.config_parameter")
        for record in self.browse(cr, uid, ids, context=context):
            config_parameters.set_param(cr, uid, "mail.catchall.virtual_alias", record.virtual_alias or '', context=context)
