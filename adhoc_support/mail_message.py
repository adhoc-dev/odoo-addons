# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2009-Today OpenERP SA (<http://www.openerp.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import osv
from osv import fields
import pooler
import re

mail_template = '''An error has occur in an OpenERP instance you are maintaining. The information of the instance and the description of the error is the following:

[Origin]

{origin}

[Prefix]

{prefix}

[Database]

{db_name}

[User ID]

{uid}

[User]

{user_name}

[Error code]

{error_code}

[Error message]

{error_message}

[Error type]

{error_data_type}

[Error debug information]

{error_data_debug}
'''

class mail_message(osv.osv):
    _name = 'mail.message'
    _inherit = 'mail.message'
    
    def send_email_support(self, cr, uid, error, origin, prefix, db_name, context=None):
        subject = 'Error in OpenERP Instance: %s' % origin if origin else 'Error in OpenERP Instance'
        
        error_code = error.get('code', '')
        error_message = error.get('message', '')
        error_data_type = error.get('data', {}).get('type', '')
        error_data_debug = error.get('data', {}).get('debug', '')
        
        user_obj = self.pool.get('res.users')
        user = user_obj.browse(cr, uid, uid, context=context)
        if isinstance(user, list):
            user = user[0]
        user_name = user.name if user else ''
        
        body = mail_template.format(origin=origin, prefix=prefix, db_name=db_name, uid=uid, user_name=user_name, error_code=error_code, error_message=error_message, error_data_type=error_data_type, error_data_debug=error_data_debug)
        attachment = {}
        
        contract_obj = self.pool.get('support.support_contract')
        contract_ids = contract_obj.search(cr, uid, [], context=context)
        
        if not contract_ids:
            message = 'You do not have defined any supporting contract. You can configure it by entering one in Settings / Publisher Warranty / Support Contract.'
            return {'correct': False, 'error_message': message}
        for contract in contract_obj.browse(cr, uid, contract_ids, context=context):
            email_to = []
            for email in contract.email_to_ids:
                email_to.append(email.email_address)
            email_from = contract.email_from
            msg_id = self.schedule_with_attach(cr, uid, email_from, email_to, subject, body, attachments=attachment, context=context)
            self.send(cr, uid, [msg_id], context=context)
        
        return {'correct': True, 'error_message': ''}
        
mail_message()


def to_email(text):
    """Return a list of the email addresses found in ``text``"""
    if not text: return []
    return re.findall(r'([^ ,<@]+@[^> ,]+)', text)

