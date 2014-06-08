# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

class support_contract(osv.osv):
    _name = 'support.support_contract'
    _description = 'Support Contract'
    
    _columns = {
        'name': fields.char('Contract Name', size=50, required=True),
        'active': fields.boolean('Active'),
        'contract_provider': fields.char('Contract Provider', size=60, required=True),
        'contract_provider_url': fields.char('Contract Provider URL', size=200, required=True),
        'email_from': fields.char('Email Sender', size=50, required=True),
        'email_to_ids' : fields.one2many('support.email', 'support_contract_id', 'Email Recipients'),
    }
    
    _defaults = {
        'active': True,
    }
    
support_contract()

class support_email(osv.osv):
    _name = 'support.email'
    _description = 'Email'
    
    _columns = {
        'name': fields.char('Name', size=30, required=True),
        'email_address': fields.char('Email Address', size=50, required=True),
        'support_contract_id': fields.many2one('support.support_contract', 'Support Contract', required=True),
    }
    
support_email()
